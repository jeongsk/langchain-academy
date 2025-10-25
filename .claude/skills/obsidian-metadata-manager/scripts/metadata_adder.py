#!/usr/bin/env python3
"""
Metadata Manager for Obsidian Vault
Adds and standardizes frontmatter metadata across markdown files.
"""

import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Directory to tag mapping
DIR_TAG_MAPPING = {
    '100 시작하기': ['getting-started', '시작하기'],
    '200 랭그래프': ['langgraph', '랭그래프'],
    '300 프롬프트 엔지니어링': ['prompt-engineering', '프롬프트'],
    '900 참고 자료': ['reference', '참고자료'],
}

# Content-based tag keywords
CONTENT_KEYWORDS = {
    'langgraph': ['LangGraph', 'ai/frameworks/langgraph'],
    'langchain': ['LangChain', 'ai/frameworks/langchain'],
    'agent': ['ai/agents'],
    'llm': ['ai/llm'],
    'tutorial': ['tutorial'],
    'ambient': ['ai/agents/ambient'],
}


class MetadataManager:
    """Manages frontmatter metadata for Obsidian vault files."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.files_processed = 0
        self.files_updated = 0

    def has_frontmatter(self, content: str) -> bool:
        """Check if file has YAML frontmatter."""
        return content.strip().startswith('---')

    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract frontmatter and body from content."""
        if not self.has_frontmatter(content):
            return None, content

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content

        frontmatter_text = parts[1].strip()
        body = parts[2].lstrip('\n')

        # Parse frontmatter
        frontmatter = {}
        current_key = None
        current_list = []

        for line in frontmatter_text.split('\n'):
            # Key-value pair
            if ':' in line and not line.strip().startswith('-'):
                if current_key and current_list:
                    frontmatter[current_key] = current_list
                    current_list = []

                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if value:
                    frontmatter[key] = value
                else:
                    current_key = key
            # List item
            elif line.strip().startswith('-'):
                item = line.strip().lstrip('-').strip()
                if item:
                    current_list.append(item)

        # Add last list if exists
        if current_key and current_list:
            frontmatter[current_key] = current_list

        return frontmatter, body

    def detect_file_type(self, file_path: Path, content: str) -> str:
        """Detect file type based on filename and content."""
        filename = file_path.stem.lower()

        # MOC detection
        if 'moc' in filename or filename == 'index':
            return 'moc'

        # Tutorial detection
        if 'tutorial' in filename or content.count('##') > 5:
            return 'tutorial'

        # Guide detection
        if 'guide' in filename or 'how-to' in filename:
            return 'guide'

        # Reference detection
        if '참고' in filename or 'reference' in filename:
            return 'reference'

        # Default
        return 'note'

    def generate_tags(self, file_path: Path, content: str) -> List[str]:
        """Generate tags based on directory and content."""
        tags = []

        # Directory-based tags
        for dir_name, dir_tags in DIR_TAG_MAPPING.items():
            if dir_name in str(file_path):
                tags.extend(dir_tags)

        # Content-based tags
        content_lower = content.lower()
        for keyword, keyword_tags in CONTENT_KEYWORDS.items():
            if keyword in content_lower:
                tags.extend(keyword_tags)

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        return unique_tags if unique_tags else ['uncategorized']

    def get_file_dates(self, file_path: Path) -> Tuple[str, str]:
        """Get creation and modification dates from filesystem."""
        stat = file_path.stat()
        created = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d')
        modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
        return created, modified

    def create_frontmatter(self, file_path: Path, content: str,
                          existing: Optional[Dict] = None) -> str:
        """Create or update frontmatter for a file."""
        if existing is None:
            existing = {}

        # Get or generate metadata
        tags = existing.get('tags', [])
        if not tags:
            tags = self.generate_tags(file_path, content)
        elif isinstance(tags, str):
            tags = [tags]

        file_type = existing.get('type', self.detect_file_type(file_path, content))
        created, modified = self.get_file_dates(file_path)
        created = existing.get('created', created)
        modified = existing.get('modified', modified)
        status = existing.get('status', 'active')

        # Build frontmatter
        frontmatter_lines = ['---']

        # Tags
        if tags:
            frontmatter_lines.append('tags:')
            for tag in tags:
                frontmatter_lines.append(f'  - {tag}')

        # Other fields
        frontmatter_lines.append(f'type: {file_type}')
        frontmatter_lines.append(f'created: {created}')
        frontmatter_lines.append(f'modified: {modified}')
        frontmatter_lines.append(f'status: {status}')
        frontmatter_lines.append('---')

        return '\n'.join(frontmatter_lines)

    def process_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """Process a single file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            self.files_processed += 1

            existing_frontmatter, body = self.extract_frontmatter(content)

            # Check if frontmatter is complete
            needs_update = False
            if existing_frontmatter is None:
                needs_update = True
            else:
                required_fields = ['tags', 'type', 'created', 'modified', 'status']
                for field in required_fields:
                    if field not in existing_frontmatter:
                        needs_update = True
                        break

            if not needs_update:
                return False

            # Create new frontmatter
            new_frontmatter = self.create_frontmatter(file_path, body, existing_frontmatter)
            new_content = f"{new_frontmatter}\n\n{body}"

            if dry_run:
                print(f"Would update: {file_path.relative_to(self.vault_path)}")
                if existing_frontmatter is None:
                    print("  Reason: No frontmatter")
                else:
                    print(f"  Reason: Missing fields")
            else:
                file_path.write_text(new_content, encoding='utf-8')
                self.files_updated += 1
                print(f"Updated: {file_path.relative_to(self.vault_path)}")

            return True

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False

    def process_vault(self, dry_run: bool = False) -> None:
        """Process all markdown files in vault."""
        for md_file in self.vault_path.rglob('*.md'):
            self.process_file(md_file, dry_run)

    def check_vault(self) -> None:
        """Check vault for files missing metadata."""
        missing_frontmatter = []
        incomplete_frontmatter = []

        for md_file in self.vault_path.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                existing, _ = self.extract_frontmatter(content)

                if existing is None:
                    missing_frontmatter.append(md_file)
                else:
                    required_fields = ['tags', 'type', 'created', 'modified', 'status']
                    missing_fields = [f for f in required_fields if f not in existing]
                    if missing_fields:
                        incomplete_frontmatter.append((md_file, missing_fields))

            except Exception as e:
                print(f"Error checking {md_file}: {e}")

        print(f"\n=== Metadata Check Results ===")
        print(f"Total files: {len(list(self.vault_path.rglob('*.md')))}")
        print(f"Files missing frontmatter: {len(missing_frontmatter)}")
        print(f"Files with incomplete frontmatter: {len(incomplete_frontmatter)}")

        if missing_frontmatter:
            print(f"\nFiles without frontmatter:")
            for file in missing_frontmatter[:10]:
                print(f"  - {file.relative_to(self.vault_path)}")
            if len(missing_frontmatter) > 10:
                print(f"  ... and {len(missing_frontmatter) - 10} more")

        if incomplete_frontmatter:
            print(f"\nFiles with incomplete frontmatter:")
            for file, missing in incomplete_frontmatter[:10]:
                print(f"  - {file.relative_to(self.vault_path)}: missing {', '.join(missing)}")
            if len(incomplete_frontmatter) > 10:
                print(f"  ... and {len(incomplete_frontmatter) - 10} more")

    def generate_report(self) -> str:
        """Generate metadata coverage report."""
        total_files = 0
        with_frontmatter = 0
        complete_frontmatter = 0

        for md_file in self.vault_path.rglob('*.md'):
            total_files += 1
            try:
                content = md_file.read_text(encoding='utf-8')
                existing, _ = self.extract_frontmatter(content)

                if existing:
                    with_frontmatter += 1
                    required_fields = ['tags', 'type', 'created', 'modified', 'status']
                    if all(f in existing for f in required_fields):
                        complete_frontmatter += 1
            except:
                pass

        report = ["# Metadata Coverage Report\n"]
        report.append(f"**Vault Path**: {self.vault_path}\n")
        report.append(f"**Total Files**: {total_files}\n")
        report.append(f"**Files with Frontmatter**: {with_frontmatter} ({with_frontmatter/total_files*100:.1f}%)\n")
        report.append(f"**Files with Complete Metadata**: {complete_frontmatter} ({complete_frontmatter/total_files*100:.1f}%)\n")

        return ''.join(report)


def main():
    parser = argparse.ArgumentParser(description='Manage metadata in Obsidian vault')
    parser.add_argument('--vault', type=Path,
                       default=Path(__file__).parent.parent.parent.parent.parent / 'docs',
                       help='Path to vault root (default: docs/)')
    parser.add_argument('--check', action='store_true',
                       help='Check which files need metadata')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making changes')
    parser.add_argument('--file', type=Path,
                       help='Process specific file only')
    parser.add_argument('--report', action='store_true',
                       help='Generate metadata coverage report')

    args = parser.parse_args()

    vault_path = args.vault.resolve()
    if not vault_path.exists():
        print(f"Error: Vault path {vault_path} does not exist")
        return 1

    manager = MetadataManager(vault_path)

    if args.check:
        manager.check_vault()
    elif args.report:
        report = manager.generate_report()
        report_path = vault_path / 'Metadata_Coverage_Report.md'
        report_path.write_text(report, encoding='utf-8')
        print(f"Report saved to: {report_path}")
        print(report)
    elif args.file:
        file_path = args.file.resolve()
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist")
            return 1
        manager.process_file(file_path, dry_run=args.dry_run)
    else:
        print(f"Processing vault at: {vault_path}")
        manager.process_vault(dry_run=args.dry_run)
        print(f"\nProcessed {manager.files_processed} files")
        if args.dry_run:
            print(f"Would update {manager.files_updated} files")
        else:
            print(f"Updated {manager.files_updated} files")


if __name__ == '__main__':
    main()
