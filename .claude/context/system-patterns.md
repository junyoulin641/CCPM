---
created: 2025-12-19T01:40:55Z
last_updated: 2025-12-19T01:40:55Z
version: 1.0
author: Claude Code PM System
---

# System Patterns

## Architectural Patterns

### PyQt6 Application Architecture

#### Single-Window Pattern
**Pattern:** Main application uses single QMainWindow as primary interface
**Implementation:** `simple-python-ui/ui/main_window.py`
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.connect_signals()
```

**Benefits:**
- Simple mental model for users
- Easy to maintain and extend
- No window management complexity
- Clear entry point

#### Event-Driven Architecture
**Pattern:** Signal-slot mechanism for UI event handling
**Implementation:**
```python
def connect_signals(self):
    """Connect button signals to handler methods."""
    self.process_btn.clicked.connect(self.handle_process)
    self.validate_btn.clicked.connect(self.handle_validate)
    self.clear_btn.clicked.connect(self.handle_clear)
```

**Benefits:**
- Decoupled UI and logic
- Clear event flow
- Easy to add new handlers
- Pythonic approach to callbacks

#### Layout-Based UI Pattern
**Pattern:** Use QVBoxLayout and QHBoxLayout instead of absolute positioning
**Implementation:**
```python
def setup_layout(self):
    """Arrange widgets in vertical layout with button row."""
    layout = QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)

    layout.addWidget(self.label)
    layout.addWidget(self.input_field)

    button_layout = QHBoxLayout()
    button_layout.addWidget(self.process_btn)
    button_layout.addWidget(self.validate_btn)
    button_layout.addWidget(self.clear_btn)

    layout.addLayout(button_layout)
```

**Benefits:**
- Responsive to window resizing
- Consistent spacing and alignment
- Maintainable UI structure
- Platform-independent positioning

### PM System Architecture

#### Command Pattern
**Pattern:** Slash commands as encapsulated operations
**Location:** `.claude/commands/pm/*.md`
**Examples:**
- `/pm:epic-sync` - Sync epic to GitHub
- `/pm:issue-start` - Start working on task
- `/pm:epic-merge` - Merge completed epic

**Benefits:**
- Consistent interface
- Composable workflows
- Self-documenting operations
- Easy to extend

#### Frontmatter Metadata Pattern
**Pattern:** YAML frontmatter in markdown files for structured metadata
**Implementation:**
```yaml
---
name: task-name
status: in-progress
created: 2025-12-18T14:30:45Z
updated: 2025-12-19T01:40:55Z
github: https://github.com/user/repo/issues/123
---
```

**Benefits:**
- Structured data in human-readable files
- Version controllable
- Easy to parse and update
- Preserves readability

#### File-Based State Management
**Pattern:** Store all state in structured markdown files
**Structure:**
```
doc/{project}/
├── prds/{feature}.md           # Feature definitions
├── epics/{feature}/
│   ├── epic-{name}.md          # Epic state
│   ├── {issue}.md              # Task state
│   └── execution-status.md     # Progress tracking
```

**Benefits:**
- No database required
- Git-friendly version control
- Human-readable and editable
- Easy backup and migration

## Design Patterns

### Separation of Concerns

#### UI Layer Separation
**Pattern:** Separate UI creation, layout, and event handling
**Methods:**
- `init_ui()` - Window configuration
- `create_widgets()` - Widget instantiation
- `setup_layout()` - Layout arrangement
- `connect_signals()` - Event wiring
- `handle_*()` - Event handlers

**Benefits:**
- Clear responsibility boundaries
- Easy to locate code
- Testable components
- Maintainable structure

#### Template Method Pattern
**Pattern:** MainWindow initialization follows consistent steps
**Implementation:**
```python
def __init__(self):
    super().__init__()
    self.init_ui()        # 1. Configure window
    self.connect_signals() # 2. Wire events
```

**Benefits:**
- Predictable initialization
- Easy to extend
- Consistent across windows
- Clear lifecycle

### Data Flow Patterns

#### Console Output Pattern
**Pattern:** Print structured console output for user feedback
**Implementation:**
```python
print(f"[Process] Original text: '{text}'")
print(f"[Validate] ✓ Valid - Input contains {len(text)} character(s)")
print("[Clear] Input field cleared")
```

**Benefits:**
- Debugging visibility
- User feedback mechanism
- Structured log format
- Easy to redirect to file

#### Input-Transform-Output Pattern
**Pattern:** Process button follows clear data flow
**Implementation:**
1. Read input: `text = self.input_field.text()`
2. Transform: `transformed = text.upper()`
3. Output: `print(f"[Process] Uppercase: '{transformed}'")`

**Benefits:**
- Functional approach
- Easy to test
- Clear data flow
- Composable transformations

## Naming Conventions

### Python Code Naming
- **Modules:** `main_window.py` (snake_case)
- **Classes:** `MainWindow` (PascalCase)
- **Methods:** `handle_process()` (snake_case with verb prefix)
- **Variables:** `input_field` (snake_case, descriptive)
- **Constants:** `WINDOW_WIDTH = 400` (UPPER_CASE if used)

### Documentation Naming
- **PRDs:** `{feature-name}.md` (kebab-case)
- **Epics:** `epic-{name}.md` (kebab-case with prefix)
- **Tasks:** `{github-issue-number}.md` (numeric)
- **Commands:** `{category}:{command}.md` (kebab-case with namespace)

### Method Naming Patterns
- **Initialization:** `init_*()` (e.g., `init_ui`)
- **Creation:** `create_*()` (e.g., `create_widgets`)
- **Setup:** `setup_*()` (e.g., `setup_layout`)
- **Event Handlers:** `handle_*()` (e.g., `handle_process`)
- **Connection:** `connect_*()` (e.g., `connect_signals`)

## Code Organization Patterns

### Package Structure
```
simple-python-ui/
├── main.py              # Entry point only
└── ui/                  # Package for UI components
    ├── __init__.py      # Package marker
    └── main_window.py   # UI implementation
```

**Pattern:** Separate entry point from implementation
**Benefits:**
- Clear module boundaries
- Importable UI components
- Scalable for multiple windows
- Clean namespace

### Import Organization
**Pattern:** Standard library → Third-party → Local
```python
import sys                           # Standard library
from PyQt6.QtWidgets import QApplication  # Third-party
from ui.main_window import MainWindow    # Local
```

**Benefits:**
- PEP 8 compliance
- Clear dependency visibility
- Easy to identify external dependencies

### Docstring Pattern
**Pattern:** Google-style docstrings for all public methods
```python
def handle_process(self):
    """
    Handle Process button click event.

    Transforms the input text and prints results to console:
    - Original text
    - Uppercase version
    - Character count
    - Reversed text
    """
```

**Benefits:**
- Self-documenting code
- IDE tooltip support
- Sphinx-compatible
- Clear expectations

## PM Workflow Patterns

### Epic Lifecycle Pattern
**Sequence:**
1. `prd-new` → Create PRD
2. `prd-parse` → Generate epic
3. `epic-decompose` → Generate tasks
4. `epic-sync` → Sync to GitHub
5. `epic-start` → Create branch and prepare
6. `issue-start` → Execute tasks (repeat for each)
7. `epic-close` → Mark complete
8. `epic-merge` → Merge to main
9. `clean` → Archive completed work

**Benefits:**
- Consistent workflow
- Clear milestones
- Traceable progress
- Automated bookkeeping

### Task Execution Pattern
**Sequence:**
1. Retrieve GitHub issue details
2. Create progress tracking directory
3. Update task status to `in_progress`
4. Create work stream file
5. Execute implementation
6. Commit changes
7. Update task status to `completed`
8. Sync to GitHub

**Benefits:**
- Traceable work
- Clear state transitions
- GitHub integration
- Documentation generation

### Branch Strategy Pattern
**Pattern:** One epic branch per feature
```bash
main → epic/{name} → [work] → merge back to main
```

**Merge Strategy:** No fast-forward (`--no-ff`)
**Benefits:**
- Preserves epic history
- Clear feature boundaries
- Easy to revert
- Visual history in git log

## Error Handling Patterns

### Validation Pattern
**Pattern:** Validate input before processing
```python
if not text:
    print("[Validate] ✗ Invalid - Input is empty")
    return
```

**Benefits:**
- Early failure detection
- Clear error messages
- Prevents invalid states
- User-friendly feedback

### Graceful Degradation
**Pattern:** Provide useful feedback even on failure
```python
# PM commands check prerequisites but continue with partial success
if not found:
    print(" File not found, using defaults")
```

**Benefits:**
- Better user experience
- Partial completion possible
- Clear failure communication
- Guidance for resolution

## Future Pattern Considerations

### State Management
For future complex state needs:
- Consider Redux/MobX-like pattern
- Centralized state store
- Immutable state updates
- Time-travel debugging

### Testing Patterns
When adding automated tests:
- Arrange-Act-Assert pattern
- Test fixtures for UI components
- Mock external dependencies
- Integration test user workflows

### Plugin Architecture
For extensibility:
- Dynamic command loading
- Plugin registration pattern
- Dependency injection
- Event bus for cross-plugin communication
