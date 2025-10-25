#!/usr/bin/env python3
"""
Link Suggester for Obsidian Vault
Discovers potential connections between notes based on entity mentions and content similarity.
"""

import argparse
from pathlib import Path
from collections import defaultdict
import re

# Key entities to track
ENTITIES = {
    'people': [
        'Harrison Chase', 'Andrew Ng', 'Sam Altman',
        'Andrej Karpathy', 'Yann LeCun',
    ],
    'technologies': [
        'LangChain', 'LangGraph', 'LangSmith',
        'OpenAI', 'Anthropic', 'Claude', 'GPT',
        'Python', 'JavaScript', 'TypeScript',
        'PostgreSQL', 'Redis', 'SQLite',
        'FAISS', 'Pinecone', 'ChromaDB',
    ],
    'concepts': [
        'agent', 'agents', 'RAG', 'embedding', 'embeddings',
        'tool calling', 'function calling', 'state management',
        'prompt engineering', 'context', 'memory',
        'multi-agent', 'subgraph', 'checkpoint',
    ],
}


class LinkAnalyzer:
    """Analyzes vault for potential link connections."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.files = {}
        self.links = defaultdict(set)
        self.backlinks = defaultdict(set)
        self.entity_mentions = defaultdict(lambda: defaultdict(set))

    def extract_wikilinks(self, content: str) -> list[str]:
        """Extract [[wikilinks]] from content."""
        pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(pattern, content)
        # Handle aliased links like [[target|alias]]
        return [m.split('|')[0].strip() for m in matches]

    def extract_entities(self, content: str) -> dict[str, set[str]]:
        """Extract entity mentions from content."""
        found = defaultdict(set)
        content_lower = content.lower()

        for category, entities in ENTITIES.items():
            for entity in entities:
                if entity.lower() in content_lower:
                    found[category].add(entity)

        return dict(found)

    def analyze_vault(self) -> None:
        """Scan all markdown files and build link/entity graph."""
        for md_file in self.vault_path.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')

                # Store file content metadata
                self.files[md_file] = {
                    'content': content,
                    'word_count': len(content.split()),
                    'outbound_links': set(),
                    'entities': {},
                }

                # Extract links
                wikilinks = self.extract_wikilinks(content)
                for link in wikilinks:
                    self.files[md_file]['outbound_links'].add(link)
                    self.links[md_file].add(link)

                    # Track backlinks
                    target_path = self._resolve_link(md_file, link)
                    if target_path:
                        self.backlinks[target_path].add(md_file)

                # Extract entities
                entities = self.extract_entities(content)
                self.files[md_file]['entities'] = entities

                # Track which files mention each entity
                for category, entity_set in entities.items():
                    for entity in entity_set:
                        self.entity_mentions[entity][category].add(md_file)

            except Exception as e:
                print(f"Error reading {md_file}: {e}")

    def _resolve_link(self, source: Path, link: str) -> Path | None:
        """Resolve a wikilink to actual file path."""
        # Simple resolution - just look for filename match
        link_filename = link + '.md'
        for file in self.files.keys():
            if file.name == link_filename:
                return file
        return None

    def find_orphans(self) -> dict[str, list[Path]]:
        """Find orphaned notes."""
        orphans = {
            'no_outbound': [],
            'no_inbound': [],
            'complete_orphans': [],
        }

        for file in self.files.keys():
            has_outbound = len(self.files[file]['outbound_links']) > 0
            has_inbound = file in self.backlinks

            if not has_outbound:
                orphans['no_outbound'].append(file)
            if not has_inbound:
                orphans['no_inbound'].append(file)
            if not has_outbound and not has_inbound:
                orphans['complete_orphans'].append(file)

        return orphans

    def find_entity_connections(self, min_shared: int = 2) -> list[tuple]:
        """Find files sharing multiple entities."""
        connections = []

        # Compare all file pairs
        file_list = list(self.files.keys())
        for i, file1 in enumerate(file_list):
            for file2 in file_list[i+1:]:
                # Count shared entities
                entities1 = self.files[file1]['entities']
                entities2 = self.files[file2]['entities']

                shared = set()
                for category in ENTITIES.keys():
                    shared.update(
                        entities1.get(category, set()) &
                        entities2.get(category, set())
                    )

                if len(shared) >= min_shared:
                    # Calculate confidence score
                    confidence = min(len(shared) / 5.0, 1.0)
                    connections.append({
                        'file1': file1,
                        'file2': file2,
                        'shared_entities': shared,
                        'confidence': confidence,
                    })

        # Sort by confidence and shared entities
        connections.sort(key=lambda x: (x['confidence'], len(x['shared_entities'])), reverse=True)
        return connections

    def find_similar_files(self) -> list[tuple]:
        """Find files with similar names or in related directories."""
        suggestions = []

        # Group by directory
        dir_groups = defaultdict(list)
        for file in self.files.keys():
            dir_groups[file.parent].append(file)

        # Suggest connections within same directory
        for directory, files in dir_groups.items():
            if len(files) > 1:
                for i, file1 in enumerate(files):
                    for file2 in files[i+1:]:
                        # Check if they already link to each other
                        if not self._are_linked(file1, file2):
                            suggestions.append({
                                'file1': file1,
                                'file2': file2,
                                'reason': f"Same directory: {directory.name}",
                                'confidence': 0.3,
                            })

        return suggestions

    def _are_linked(self, file1: Path, file2: Path) -> bool:
        """Check if two files are linked in either direction."""
        file1_links_to_2 = file2 in self.backlinks.get(file2, set())
        file2_links_to_1 = file1 in self.backlinks.get(file1, set())
        return file1_links_to_2 or file2_links_to_1

    def generate_report(self) -> str:
        """Generate link suggestions report."""
        report = ["# Link Suggestions Report\n"]
        report.append(f"**Vault Path**: {self.vault_path}\n")
        report.append(f"**Total Files**: {len(self.files)}\n")
        report.append(f"**Total Links**: {sum(len(links) for links in self.links.values())}\n\n")

        # Orphans
        orphans = self.find_orphans()
        report.append("## Orphaned Notes\n")
        report.append(f"- **Complete orphans** (no links in/out): {len(orphans['complete_orphans'])}\n")
        report.append(f"- **No outbound links**: {len(orphans['no_outbound'])}\n")
        report.append(f"- **No inbound links**: {len(orphans['no_inbound'])}\n\n")

        if orphans['complete_orphans']:
            report.append("### Complete Orphans\n")
            for file in orphans['complete_orphans'][:10]:
                report.append(f"- {file.relative_to(self.vault_path)}\n")
            if len(orphans['complete_orphans']) > 10:
                report.append(f"  ... and {len(orphans['complete_orphans']) - 10} more\n")
            report.append("\n")

        # Entity-based connections
        connections = self.find_entity_connections()
        report.append("## Entity-Based Connection Suggestions\n")
        report.append(f"Found {len(connections)} potential connections based on shared entities\n\n")

        # High confidence
        high_conf = [c for c in connections if c['confidence'] > 0.7]
        if high_conf:
            report.append("### High Confidence (>0.7)\n")
            for conn in high_conf[:10]:
                file1 = conn['file1'].relative_to(self.vault_path)
                file2 = conn['file2'].relative_to(self.vault_path)
                entities = ', '.join(conn['shared_entities'])
                report.append(f"\n**{file1}** ↔ **{file2}**\n")
                report.append(f"- Confidence: {conn['confidence']:.2f}\n")
                report.append(f"- Shared entities: {entities}\n")

        # Medium confidence
        med_conf = [c for c in connections if 0.4 <= c['confidence'] <= 0.7]
        if med_conf:
            report.append("\n### Medium Confidence (0.4-0.7)\n")
            for conn in med_conf[:10]:
                file1 = conn['file1'].relative_to(self.vault_path)
                file2 = conn['file2'].relative_to(self.vault_path)
                entities = ', '.join(conn['shared_entities'])
                report.append(f"\n**{file1}** ↔ **{file2}**\n")
                report.append(f"- Confidence: {conn['confidence']:.2f}\n")
                report.append(f"- Shared entities: {entities}\n")

        # Entity usage stats
        report.append("\n## Entity Mentions\n")
        entity_stats = []
        for entity, mentions in self.entity_mentions.items():
            total_files = sum(len(files) for files in mentions.values())
            entity_stats.append((entity, total_files))

        entity_stats.sort(key=lambda x: x[1], reverse=True)
        for entity, count in entity_stats[:15]:
            report.append(f"- **{entity}**: {count} files\n")

        return ''.join(report)


def main():
    parser = argparse.ArgumentParser(description='Suggest links between related notes')
    parser.add_argument('--vault', type=Path,
                       default=Path(__file__).parent.parent.parent.parent.parent / 'docs',
                       help='Path to vault root (default: docs/)')
    parser.add_argument('--orphans', action='store_true',
                       help='Show orphaned notes only')
    parser.add_argument('--entities', action='store_true',
                       help='Show entity-based connections only')
    parser.add_argument('--output', type=Path,
                       help='Output file for report (default: stdout)')

    args = parser.parse_args()

    vault_path = args.vault.resolve()
    if not vault_path.exists():
        print(f"Error: Vault path {vault_path} does not exist")
        return 1

    print(f"Analyzing vault at: {vault_path}")
    analyzer = LinkAnalyzer(vault_path)
    analyzer.analyze_vault()

    if args.orphans:
        orphans = analyzer.find_orphans()
        print(f"\n=== Orphaned Notes ===")
        print(f"Complete orphans: {len(orphans['complete_orphans'])}")
        print(f"No outbound links: {len(orphans['no_outbound'])}")
        print(f"No inbound links: {len(orphans['no_inbound'])}")

        if orphans['complete_orphans']:
            print("\nComplete orphans:")
            for file in orphans['complete_orphans']:
                print(f"  - {file.relative_to(vault_path)}")

    elif args.entities:
        connections = analyzer.find_entity_connections()
        print(f"\n=== Entity-Based Connections ===")
        print(f"Found {len(connections)} potential connections")

        for conn in connections[:20]:
            file1 = conn['file1'].relative_to(vault_path)
            file2 = conn['file2'].relative_to(vault_path)
            entities = ', '.join(conn['shared_entities'])
            print(f"\n{file1} ↔ {file2}")
            print(f"  Confidence: {conn['confidence']:.2f}")
            print(f"  Shared: {entities}")

    else:
        # Full report
        report = analyzer.generate_report()

        if args.output:
            args.output.write_text(report, encoding='utf-8')
            print(f"\nReport saved to: {args.output}")
        else:
            print(report)


if __name__ == '__main__':
    main()
