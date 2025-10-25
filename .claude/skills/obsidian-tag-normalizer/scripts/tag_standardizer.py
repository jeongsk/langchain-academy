#!/usr/bin/env python3
"""
Tag Standardizer for Obsidian Vault
Analyzes and standardizes tags across markdown files in the vault.
"""

import re
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Tag normalization rules
TAG_MAPPINGS = {
    # Technology names - proper casing
    'langchain': 'LangChain',
    'langgraph': 'LangGraph',
    'openai': 'OpenAI',
    'anthropic': 'Anthropic',
    'claude': 'Claude',
    'postgresql': 'PostgreSQL',
    'javascript': 'JavaScript',
    'typescript': 'TypeScript',
    'python': 'Python',

    # Common variations to hierarchical
    'ai-agents': 'ai/agents',
    'ai-llm': 'ai/llm',
    'ai-embeddings': 'ai/embeddings',
}


class TagAnalyzer:
    """Analyzes tags across the vault."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.tag_usage: Dict[str, List[Path]] = defaultdict(list)
        self.file_tags: Dict[Path, List[str]] = {}

    def extract_frontmatter_tags(self, content: str) -> List[str]:
        """Extract tags from YAML frontmatter."""
        tags = []
        in_frontmatter = False
        in_tags_section = False

        for line in content.split('\n'):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    break
                continue

            if in_frontmatter:
                if line.startswith('tags:'):
                    # Inline tags: tags: [tag1, tag2]
                    inline_match = re.search(r'tags:\s*\[(.*?)\]', line)
                    if inline_match:
                        tag_str = inline_match.group(1)
                        tags.extend([t.strip().strip('"\'') for t in tag_str.split(',')])
                    else:
                        in_tags_section = True
                elif in_tags_section:
                    if line.startswith('  -') or line.startswith('- '):
                        tag = line.strip().lstrip('-').strip()
                        if tag:
                            tags.append(tag)
                    elif not line.startswith(' '):
                        in_tags_section = False

        return tags

    def analyze_vault(self) -> None:
        """Scan all markdown files and extract tags."""
        for md_file in self.vault_path.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                tags = self.extract_frontmatter_tags(content)

                if tags:
                    self.file_tags[md_file] = tags
                    for tag in tags:
                        self.tag_usage[tag].append(md_file)

            except Exception as e:
                print(f"Error reading {md_file}: {e}")

    def find_inconsistencies(self) -> Dict[str, List[str]]:
        """Find tags that should be normalized."""
        issues = defaultdict(list)

        all_tags = set(self.tag_usage.keys())

        for tag in all_tags:
            # Check for case variations
            similar_tags = [t for t in all_tags
                          if t.lower() == tag.lower() and t != tag]
            if similar_tags:
                issues['case_inconsistency'].extend([tag] + similar_tags)

            # Check for known mappings
            if tag.lower() in TAG_MAPPINGS:
                expected = TAG_MAPPINGS[tag.lower()]
                if tag != expected:
                    issues['should_map'].append(f"{tag} → {expected}")

            # Check for potential hierarchical structure
            if '-' in tag and '/' not in tag:
                parts = tag.split('-')
                if len(parts) == 2:
                    potential = f"{parts[0]}/{parts[1]}"
                    issues['potential_hierarchical'].append(f"{tag} → {potential}")

        return dict(issues)

    def generate_report(self) -> str:
        """Generate a markdown report of tag analysis."""
        report = ["# Tag Analysis Report\n"]
        report.append(f"**Vault Path**: {self.vault_path}\n")
        report.append(f"**Total Files with Tags**: {len(self.file_tags)}\n")
        report.append(f"**Unique Tags**: {len(self.tag_usage)}\n\n")

        # Tag frequency
        report.append("## Tag Usage Frequency\n")
        sorted_tags = sorted(self.tag_usage.items(),
                           key=lambda x: len(x[1]), reverse=True)
        for tag, files in sorted_tags[:20]:
            report.append(f"- `{tag}`: {len(files)} files\n")

        # Inconsistencies
        issues = self.find_inconsistencies()
        if issues:
            report.append("\n## Inconsistencies Found\n")

            if 'case_inconsistency' in issues:
                report.append("\n### Case Inconsistencies\n")
                unique_cases = list(set(issues['case_inconsistency']))
                report.append(f"Found {len(unique_cases)} tags with case variations\n")
                for tag in unique_cases[:10]:
                    report.append(f"- `{tag}`\n")

            if 'should_map' in issues:
                report.append("\n### Recommended Mappings\n")
                for mapping in issues['should_map']:
                    report.append(f"- {mapping}\n")

            if 'potential_hierarchical' in issues:
                report.append("\n### Potential Hierarchical Tags\n")
                for suggestion in issues['potential_hierarchical'][:10]:
                    report.append(f"- {suggestion}\n")

        return ''.join(report)


class TagStandardizer:
    """Applies tag standardization to files."""

    def __init__(self, analyzer: TagAnalyzer):
        self.analyzer = analyzer
        self.changes_made = 0

    def normalize_tag(self, tag: str) -> str:
        """Normalize a single tag based on rules."""
        # Check direct mapping
        if tag.lower() in TAG_MAPPINGS:
            return TAG_MAPPINGS[tag.lower()]

        # Check for case-only variations
        for known_tag in TAG_MAPPINGS.values():
            if tag.lower() == known_tag.lower():
                return known_tag

        return tag

    def update_file_tags(self, file_path: Path, dry_run: bool = False) -> bool:
        """Update tags in a single file."""
        content = file_path.read_text(encoding='utf-8')
        original_tags = self.analyzer.file_tags.get(file_path, [])

        if not original_tags:
            return False

        normalized_tags = [self.normalize_tag(tag) for tag in original_tags]

        if original_tags == normalized_tags:
            return False

        # Replace tags in frontmatter
        new_content = self._replace_frontmatter_tags(content, original_tags, normalized_tags)

        if not dry_run:
            file_path.write_text(new_content, encoding='utf-8')
            self.changes_made += 1
            print(f"Updated: {file_path.relative_to(self.analyzer.vault_path)}")
            for old, new in zip(original_tags, normalized_tags):
                if old != new:
                    print(f"  {old} → {new}")
        else:
            print(f"Would update: {file_path.relative_to(self.analyzer.vault_path)}")
            for old, new in zip(original_tags, normalized_tags):
                if old != new:
                    print(f"  {old} → {new}")

        return True

    def _replace_frontmatter_tags(self, content: str, old_tags: List[str], new_tags: List[str]) -> str:
        """Replace tags in YAML frontmatter."""
        lines = content.split('\n')
        new_lines = []
        in_frontmatter = False
        in_tags_section = False
        tag_idx = 0

        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    in_frontmatter = False
                new_lines.append(line)
                continue

            if in_frontmatter:
                if line.startswith('tags:'):
                    # Handle inline tags
                    inline_match = re.search(r'tags:\s*\[(.*?)\]', line)
                    if inline_match:
                        new_lines.append(f"tags: [{', '.join(new_tags)}]")
                    else:
                        in_tags_section = True
                        new_lines.append(line)
                elif in_tags_section:
                    if (line.startswith('  -') or line.startswith('- ')) and tag_idx < len(new_tags):
                        indent = '  ' if line.startswith('  ') else ''
                        new_lines.append(f"{indent}- {new_tags[tag_idx]}")
                        tag_idx += 1
                    elif not line.startswith(' '):
                        in_tags_section = False
                        new_lines.append(line)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        return '\n'.join(new_lines)

    def standardize_all(self, dry_run: bool = False) -> int:
        """Standardize tags across all files."""
        for file_path in self.analyzer.file_tags.keys():
            self.update_file_tags(file_path, dry_run)

        return self.changes_made


def main():
    parser = argparse.ArgumentParser(description='Standardize tags in Obsidian vault')
    parser.add_argument('--vault', type=Path,
                       default=Path(__file__).parent.parent.parent.parent.parent / 'docs',
                       help='Path to vault root (default: docs/)')
    parser.add_argument('--report', action='store_true',
                       help='Generate analysis report only')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making changes')

    args = parser.parse_args()

    vault_path = args.vault.resolve()
    if not vault_path.exists():
        print(f"Error: Vault path {vault_path} does not exist")
        return 1

    print(f"Analyzing vault at: {vault_path}")
    analyzer = TagAnalyzer(vault_path)
    analyzer.analyze_vault()

    if args.report:
        report = analyzer.generate_report()
        report_path = vault_path / 'Tag_Analysis_Report.md'
        report_path.write_text(report, encoding='utf-8')
        print(f"\nReport saved to: {report_path}")
        print(report)
    else:
        standardizer = TagStandardizer(analyzer)
        changes = standardizer.standardize_all(dry_run=args.dry_run)

        if args.dry_run:
            print(f"\nDry run complete. Would update {changes} files.")
        else:
            print(f"\nStandardization complete. Updated {changes} files.")


if __name__ == '__main__':
    main()
