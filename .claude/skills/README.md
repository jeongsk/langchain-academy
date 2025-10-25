# Claude Code Skills for Obsidian Vault Management

This directory contains Claude Code Skills for managing Obsidian vaults. These skills are automatically invoked by Claude when working with markdown documentation.

## Available Skills

### 1. obsidian-tag-normalizer
**Purpose**: Normalize and standardize tags across the vault
**Use Cases**:
- Fix inconsistent tag capitalization (langchain → LangChain)
- Convert flat tags to hierarchical (ai-agents → ai/agents)
- Consolidate duplicate tags
- Maintain tag taxonomy

**Script**: `obsidian-tag-normalizer/scripts/tag_standardizer.py`

**Usage**:
```bash
# Generate tag analysis report
python3 .claude/skills/obsidian-tag-normalizer/scripts/tag_standardizer.py --report

# Preview changes
python3 .claude/skills/obsidian-tag-normalizer/scripts/tag_standardizer.py --dry-run

# Apply standardization
python3 .claude/skills/obsidian-tag-normalizer/scripts/tag_standardizer.py
```

---

### 2. obsidian-metadata-manager
**Purpose**: Add and standardize frontmatter metadata
**Use Cases**:
- Add missing frontmatter to markdown files
- Standardize metadata fields (tags, type, dates, status)
- Auto-generate tags from directory structure
- Ensure consistent file types

**Script**: `obsidian-metadata-manager/scripts/metadata_adder.py`

**Usage**:
```bash
# Check which files need metadata
python3 .claude/skills/obsidian-metadata-manager/scripts/metadata_adder.py --check

# Preview changes
python3 .claude/skills/obsidian-metadata-manager/scripts/metadata_adder.py --dry-run

# Apply metadata updates
python3 .claude/skills/obsidian-metadata-manager/scripts/metadata_adder.py

# Process specific file
python3 .claude/skills/obsidian-metadata-manager/scripts/metadata_adder.py --file "path/to/file.md"
```

---

### 3. obsidian-content-curator
**Purpose**: Maintain content quality and organization
**Use Cases**:
- Identify stub notes (< 100 words)
- Find duplicate or redundant content
- Detect outdated information
- Suggest content improvements
- Consolidate similar notes

**Script**: No automated script (manual curation focus)

**Process**:
- Analyzes content quality metrics
- Suggests consolidation opportunities
- Identifies stale content
- Provides improvement recommendations

---

### 4. obsidian-link-suggester
**Purpose**: Discover connections between related notes
**Use Cases**:
- Find orphaned notes (no incoming/outgoing links)
- Suggest links based on shared entities
- Identify content with keyword overlap
- Build knowledge graph connections

**Script**: `obsidian-link-suggester/scripts/link_suggester.py`

**Usage**:
```bash
# Generate full link suggestions report
python3 .claude/skills/obsidian-link-suggester/scripts/link_suggester.py

# Show orphaned notes only
python3 .claude/skills/obsidian-link-suggester/scripts/link_suggester.py --orphans

# Show entity-based connections
python3 .claude/skills/obsidian-link-suggester/scripts/link_suggester.py --entities

# Save report to file
python3 .claude/skills/obsidian-link-suggester/scripts/link_suggester.py --output report.md
```

---

### 5. obsidian-moc-creator
**Purpose**: Create and maintain Maps of Content (MOCs)
**Use Cases**:
- Generate index pages for directories
- Create navigation hubs for topics
- Organize content hierarchically
- Maintain MOC network structure

**Script**: `obsidian-moc-creator/scripts/moc_generator.py`

**Usage**:
```bash
# Find directories needing MOCs
python3 .claude/skills/obsidian-moc-creator/scripts/moc_generator.py --suggest

# Create MOC for specific directory
python3 .claude/skills/obsidian-moc-creator/scripts/moc_generator.py \
    --directory "docs/200 랭그래프" \
    --title "LangGraph"

# Create all suggested MOCs
python3 .claude/skills/obsidian-moc-creator/scripts/moc_generator.py --create-all

# Generate MOC coverage report
python3 .claude/skills/obsidian-moc-creator/scripts/moc_generator.py --report
```

---

## How Skills Work

Unlike slash commands (which you invoke manually), **Skills are automatically invoked by Claude** when they're relevant to the task at hand.

### Automatic Invocation

Claude will use these skills when:
- Working with markdown files in `docs/`
- You mention tags, metadata, or organization
- Discussing content quality or structure
- Working with links between notes
- Creating navigation or index pages

### Skill vs Agent

**Skills** (`.claude/skills/`):
- Model-invoked (automatic)
- Used by Claude when relevant
- Defined by SKILL.md files

**Agents** (`.claude/agents/`):
- Explicitly invoked via Task tool
- More control over when they run
- Used for complex multi-step workflows

This project has **both** - agents for explicit invocation and skills for automatic use.

## Project-Specific Features

These skills are adapted for this LangGraph Academy repository:

### Korean/English Support
- Handles both Korean and English content
- Bilingual tag normalization
- Cross-language content linking
- Maintains consistency across languages

### Educational Content Focus
- Optimized for tutorial sequences
- Supports learning path organization
- Handles numbered modules and projects
- Links conceptual and practical content

### LangGraph Specific
- Recognizes LangGraph terminology
- Tags for AI/ML concepts
- Organizes by module structure
- Links studio implementations to tutorials

## Directory Structure

```
.claude/skills/
├── obsidian-tag-normalizer/
│   ├── SKILL.md
│   └── scripts/
│       └── tag_standardizer.py
├── obsidian-metadata-manager/
│   ├── SKILL.md
│   └── scripts/
│       └── metadata_adder.py
├── obsidian-content-curator/
│   └── SKILL.md
├── obsidian-link-suggester/
│   ├── SKILL.md
│   └── scripts/
│       └── link_suggester.py
└── obsidian-moc-creator/
    ├── SKILL.md
    └── scripts/
        └── moc_generator.py
```

## Script Requirements

All Python scripts require Python 3.10+ and use only standard library modules (no external dependencies).

To make scripts executable:
```bash
chmod +x .claude/skills/*/scripts/*.py
```

## Workflow Example

### Complete Vault Maintenance Workflow

```bash
# 1. Check metadata coverage
python3 .claude/skills/obsidian-metadata-manager/scripts/metadata_adder.py --check

# 2. Add missing metadata
python3 .claude/skills/obsidian-metadata-manager/scripts/metadata_adder.py

# 3. Normalize tags
python3 .claude/skills/obsidian-tag-normalizer/scripts/tag_standardizer.py

# 4. Find orphaned notes
python3 .claude/skills/obsidian-link-suggester/scripts/link_suggester.py --orphans

# 5. Create missing MOCs
python3 .claude/skills/obsidian-moc-creator/scripts/moc_generator.py --suggest
python3 .claude/skills/obsidian-moc-creator/scripts/moc_generator.py --create-all
```

## Related Files

- `.claude/agents/` - Task-invoked agents for complex workflows
- `.claude/CLAUDE.md` - Project-specific Claude Code instructions
- `docs/` - Vault content these skills manage

## Skill Development

To add new skills:

1. Create directory in `.claude/skills/skill-name/`
2. Write `SKILL.md` with required frontmatter:
   ```yaml
   ---
   name: skill-name
   description: What it does and when to use it
   allowed-tools: Read, Write, Bash, Glob, Grep
   ---
   ```
3. Add detailed instructions in markdown
4. Optionally create supporting scripts in `scripts/` subdirectory

See [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills) for more details.
