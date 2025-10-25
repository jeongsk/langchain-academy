#!/usr/bin/env python3
"""
MOC (Map of Content) Generator for Obsidian Vault
Automatically generates navigation hubs for directories.
"""

import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

MOC_TEMPLATE = """---
tags:
  - moc
  - {tag}
type: moc
created: {created}
modified: {modified}
status: active
---

# {title}

{description}

## Overview

This section organizes content related to {topic}.

{sections}

## Related Topics

{related}

---

**Last Updated**: {modified}
**Auto-generated**: This MOC was automatically generated and may need manual refinement.
"""


class MOCGenerator:
    """Generates Maps of Content for directories."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path

    def has_moc(self, directory: Path) -> bool:
        """Check if directory already has a MOC/index file."""
        moc_candidates = [
            'index.md',
            'README.md',
        ]

        for candidate in moc_candidates:
            if (directory / candidate).exists():
                return True

        # Check for any file starting with "MOC -"
        for file in directory.glob('MOC - *.md'):
            return True

        return False

    def find_directories_needing_mocs(self, min_files: int = 5) -> list[tuple]:
        """Find directories that could benefit from MOCs."""
        candidates = []

        for directory in self.vault_path.rglob('*'):
            if not directory.is_dir():
                continue

            # Skip hidden directories
            if any(part.startswith('.') for part in directory.parts):
                continue

            # Count markdown files
            md_files = list(directory.glob('*.md'))

            if len(md_files) >= min_files and not self.has_moc(directory):
                candidates.append({
                    'directory': directory,
                    'file_count': len(md_files),
                    'files': md_files,
                })

        candidates.sort(key=lambda x: x['file_count'], reverse=True)
        return candidates

    def analyze_directory_content(self, directory: Path) -> dict:
        """Analyze content in a directory to determine MOC structure."""
        md_files = sorted(directory.glob('*.md'))

        analysis = {
            'files': md_files,
            'categories': defaultdict(list),
            'sequences': [],
            'has_korean': False,
            'has_english': False,
        }

        # Categorize files
        for file in md_files:
            filename = file.stem

            # Check language
            if any(ord(c) > 127 for c in filename):  # Simple Korean detection
                analysis['has_korean'] = True
            else:
                analysis['has_english'] = True

            # Categorize by filename patterns
            if '개념' in filename or 'concept' in filename.lower():
                analysis['categories']['Concepts'].append(file)
            elif '튜토리얼' in filename or 'tutorial' in filename.lower():
                analysis['categories']['Tutorials'].append(file)
            elif '가이드' in filename or 'guide' in filename.lower():
                analysis['categories']['Guides'].append(file)
            elif '참고' in filename or 'reference' in filename.lower():
                analysis['categories']['References'].append(file)
            elif '에이전트' in filename or 'agent' in filename.lower():
                analysis['categories']['Agents'].append(file)
            else:
                analysis['categories']['Other'].append(file)

        # Detect number sequences (e.g., 1-intro.md, 2-setup.md)
        numbered = [f for f in md_files if f.stem[0].isdigit()]
        if len(numbered) > 2:
            analysis['sequences'] = sorted(numbered)

        return analysis

    def generate_moc_content(self, directory: Path, title: str = None,
                           description: str = None) -> str:
        """Generate MOC content for a directory."""
        analysis = self.analyze_directory_content(directory)

        # Determine title
        if not title:
            title = directory.name

        # Generate tag from title
        tag = title.lower().replace(' ', '-').replace('/', '-')

        # Default description
        if not description:
            description = f"Navigation hub for {title} content."

        # Build sections
        sections_list = []

        # If there's a sequence, show it first
        if analysis['sequences']:
            sections_list.append("## Learning Sequence\n")
            for i, file in enumerate(analysis['sequences'], 1):
                link = f"[[{file.stem}]]"
                sections_list.append(f"{i}. {link}\n")
            sections_list.append("\n")

        # Show categorized content
        for category, files in sorted(analysis['categories'].items()):
            if not files:
                continue

            # Skip "Other" if we have other categories
            if category == "Other" and len(analysis['categories']) > 1:
                continue

            # Translate category names to bilingual if needed
            if analysis['has_korean'] and analysis['has_english']:
                category_map = {
                    'Concepts': 'Concepts / 개념',
                    'Tutorials': 'Tutorials / 튜토리얼',
                    'Guides': 'Guides / 가이드',
                    'References': 'References / 참고자료',
                    'Agents': 'Agents / 에이전트',
                }
                category_name = category_map.get(category, category)
            else:
                category_name = category

            sections_list.append(f"## {category_name}\n\n")
            for file in sorted(files):
                link = f"[[{file.stem}]]"
                sections_list.append(f"- {link}\n")
            sections_list.append("\n")

        sections = ''.join(sections_list) if sections_list else "## Content\n\nContent will be organized here.\n"

        # Find related directories for cross-references
        parent = directory.parent
        siblings = [d for d in parent.iterdir()
                   if d.is_dir() and d != directory
                   and not d.name.startswith('.')]

        related_links = []
        for sibling in siblings[:5]:  # Limit to 5 related
            sibling_moc = sibling / 'index.md'
            if sibling_moc.exists():
                related_links.append(f"- [[{sibling.name}/index|{sibling.name}]]")

        related = '\n'.join(related_links) if related_links else "- [[index|Main Index]]"

        # Generate dates
        today = datetime.now().strftime('%Y-%m-%d')

        # Fill template
        content = MOC_TEMPLATE.format(
            tag=tag,
            title=title,
            description=description,
            topic=title,
            sections=sections,
            related=related,
            created=today,
            modified=today,
        )

        return content

    def create_moc(self, directory: Path, title: str = None,
                  filename: str = "index.md") -> Path:
        """Create MOC file for a directory."""
        content = self.generate_moc_content(directory, title)
        moc_path = directory / filename
        moc_path.write_text(content, encoding='utf-8')
        return moc_path

    def generate_report(self) -> str:
        """Generate report of directories needing MOCs."""
        candidates = self.find_directories_needing_mocs()

        report = ["# MOC Generation Report\n"]
        report.append(f"**Vault Path**: {self.vault_path}\n")
        report.append(f"**Directories Needing MOCs**: {len(candidates)}\n\n")

        if candidates:
            report.append("## Suggested MOCs\n\n")
            for candidate in candidates:
                dir_path = candidate['directory'].relative_to(self.vault_path)
                count = candidate['file_count']
                report.append(f"### {dir_path}\n")
                report.append(f"- **Files**: {count}\n")
                report.append(f"- **Suggested Title**: {candidate['directory'].name}\n\n")

        return ''.join(report)


def main():
    parser = argparse.ArgumentParser(description='Generate MOCs for Obsidian vault')
    parser.add_argument('--vault', type=Path,
                       default=Path(__file__).parent.parent.parent.parent.parent / 'docs',
                       help='Path to vault root (default: docs/)')
    parser.add_argument('--suggest', action='store_true',
                       help='Show directories that need MOCs')
    parser.add_argument('--directory', type=str,
                       help='Create MOC for specific directory (relative to vault)')
    parser.add_argument('--title', type=str,
                       help='Title for the MOC (default: directory name)')
    parser.add_argument('--create-all', action='store_true',
                       help='Create MOCs for all suggested directories')
    parser.add_argument('--report', action='store_true',
                       help='Generate MOC coverage report')
    parser.add_argument('--min-files', type=int, default=5,
                       help='Minimum files for MOC suggestion (default: 5)')

    args = parser.parse_args()

    vault_path = args.vault.resolve()
    if not vault_path.exists():
        print(f"Error: Vault path {vault_path} does not exist")
        return 1

    generator = MOCGenerator(vault_path)

    if args.suggest or args.report:
        report = generator.generate_report()
        print(report)

        if args.report:
            report_path = vault_path / 'MOC_Generation_Report.md'
            report_path.write_text(report, encoding='utf-8')
            print(f"\nReport saved to: {report_path}")

    elif args.directory:
        dir_path = vault_path / args.directory
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"Error: Directory {dir_path} does not exist")
            return 1

        title = args.title or dir_path.name
        moc_path = generator.create_moc(dir_path, title)
        print(f"Created MOC: {moc_path.relative_to(vault_path)}")

    elif args.create_all:
        candidates = generator.find_directories_needing_mocs(min_files=args.min_files)
        print(f"Creating MOCs for {len(candidates)} directories...\n")

        for candidate in candidates:
            directory = candidate['directory']
            title = directory.name
            try:
                moc_path = generator.create_moc(directory, title)
                print(f"✓ Created: {moc_path.relative_to(vault_path)}")
            except Exception as e:
                print(f"✗ Failed: {directory.relative_to(vault_path)} - {e}")

        print(f"\nCreated MOCs for {len(candidates)} directories")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
