---
created: 2025-12-19T01:40:55Z
last_updated: 2025-12-19T01:40:55Z
version: 1.0
author: Claude Code PM System
---

# Project Structure

## Root Directory Layout

```
CCPM/
├── .claude/                    # Claude Code PM system configuration
│   ├── agents/                 # Custom agent definitions
│   ├── commands/               # Slash command implementations
│   │   ├── context/           # Context management commands
│   │   └── pm/                # Project management commands
│   ├── context/               # Project context documentation (this directory)
│   ├── rules/                 # Standard operating procedures
│   └── skills/                # Reusable skills and capabilities
├── .git/                      # Git repository data
├── doc/                       # Project documentation and PM artifacts
│   └── simple-python-ui/      # Documentation for simple-python-ui project
│       ├── epics/             # Epic and task documentation
│       │   └── basic-ui/      # Basic UI feature epic
│       │       └── .archived/ # Completed/archived epic files
│       ├── prds/              # Product requirement documents
│       └── PROJECT-PRD.md     # Master project PRD
├── simple-python-ui/          # PyQt6 desktop application
│   ├── ui/                    # UI components package
│   │   ├── __init__.py        # Package initialization
│   │   └── main_window.py     # Main window class
│   ├── main.py                # Application entry point
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Application documentation
└── README.md                  # Repository root README
```

## Key Directories

### .claude/ - PM System Configuration
**Purpose:** Houses the Claude Code Project Management system
**Key Files:**
- `agents/code-reviewer.md` - Code review agent definition
- `commands/pm/*.md` - 20+ PM commands (epic-sync, issue-start, etc.)
- `commands/context/*.md` - Context management commands
- `rules/*.md` - Standard operating procedures and patterns

**File Naming Convention:** kebab-case with .md extension

### doc/ - Documentation Repository
**Purpose:** Stores all project management artifacts and documentation
**Structure:**
- `{project-name}/prds/` - Product requirement documents
- `{project-name}/epics/{feature}/` - Epic and task files
- `{project-name}/epics/{feature}/.archived/` - Completed work archive

**Frontmatter:** All markdown files include YAML frontmatter with metadata

### simple-python-ui/ - Application Code
**Purpose:** PyQt6 desktop application codebase
**Structure:**
- Root level: Entry point (main.py) and configuration files
- `ui/` package: UI components and window classes
- Standard Python package structure with `__init__.py` files

**Naming Conventions:**
- Python files: snake_case.py
- Classes: PascalCase (e.g., MainWindow)
- Methods/functions: snake_case

## File Organization Patterns

### Python Application Structure
```
simple-python-ui/
├── main.py              # Entry point with main() function
├── requirements.txt     # Dependency specification
├── README.md           # User-facing documentation
└── ui/                 # Package directory
    ├── __init__.py     # Package initialization
    └── main_window.py  # UI class implementation
```

### Documentation Structure
```
doc/{project}/
├── PROJECT-PRD.md              # Master PRD
├── prds/{feature}.md           # Feature PRDs
└── epics/{feature}/
    ├── epic-{name}.md          # Epic definition
    ├── {issue}.md              # Task files (numbered by GitHub issue)
    ├── execution-status.md     # Epic progress tracking
    ├── github-mapping.md       # GitHub sync metadata
    └── updates/{issue}/        # Task progress files
        └── stream-{X}.md       # Work stream documentation
```

### Archive Structure
Completed epics moved to `.archived/` directory with:
- Original epic file
- All task files
- Progress tracking files
- `archive-log.md` documenting completion

## Module Organization

### Claude PM System Modules
- **Commands:** Organized by category (pm/, context/)
- **Agents:** Specialized AI agents for specific tasks
- **Rules:** Reusable patterns and standards
- **Skills:** Domain-specific capabilities

### Application Modules
- **UI Package:** Contains all PyQt6 UI components
- **Entry Point:** Minimal main.py for application bootstrap
- **Configuration:** Requirements and metadata in root

## File Naming Standards

### Python Code
- Modules: `lowercase_with_underscores.py`
- Classes: `PascalCase`
- Functions/Methods: `snake_case`

### Documentation
- PRDs: `{feature-name}.md`
- Epics: `epic-{name}.md`
- Tasks: `{github-issue-number}.md`
- Commands: `{command-name}.md`

### Configuration
- Python: `requirements.txt`, `pyproject.toml`
- Git: `.gitignore`, `.git/`
- System: `.claude/`

## Growth Patterns

### Adding New Features
1. Create PRD in `doc/{project}/prds/{feature}.md`
2. Decompose to epic in `doc/{project}/epics/{feature}/epic-{name}.md`
3. Generate task files as `{issue-number}.md`
4. Implement in application code directory
5. Archive completed epic to `.archived/`

### Scaling Project Structure
- Multiple projects: Add sibling directories to `simple-python-ui/`
- Multiple features: Add epics under `doc/{project}/epics/`
- Modular UI: Add subpackages under `simple-python-ui/ui/`
