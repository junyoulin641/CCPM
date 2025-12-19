---
created: 2025-12-19T01:40:55Z
last_updated: 2025-12-19T01:40:55Z
version: 1.0
author: Claude Code PM System
---

# Project Style Guide

## Python Code Standards

### PEP 8 Compliance
All Python code MUST follow PEP 8 guidelines: https://peps.python.org/pep-0008/

**Key Requirements:**
- 4 spaces for indentation (no tabs)
- Maximum line length: 79 characters for code, 72 for docstrings
- Two blank lines between top-level functions and classes
- One blank line between methods in a class
- Imports organized: standard library → third-party → local

### Naming Conventions

#### Modules and Files
- **Format:** `lowercase_with_underscores.py`
- **Examples:**
  - `main_window.py`
  - `data_processor.py`
  - `config_handler.py`

#### Classes
- **Format:** `PascalCase` (CapWords)
- **Examples:**
  - `class MainWindow(QMainWindow):`
  - `class DataProcessor:`
  - `class ConfigHandler:`

#### Functions and Methods
- **Format:** `lowercase_with_underscores`
- **Prefix conventions:**
  - `init_*` - Initialization methods (e.g., `init_ui`)
  - `create_*` - Creation methods (e.g., `create_widgets`)
  - `setup_*` - Setup/configuration methods (e.g., `setup_layout`)
  - `handle_*` - Event handlers (e.g., `handle_process`)
  - `connect_*` - Signal connection methods (e.g., `connect_signals`)
  - `validate_*` - Validation methods (e.g., `validate_input`)
  - `get_*` - Getter methods (e.g., `get_text`)
  - `set_*` - Setter methods (e.g., `set_text`)

**Examples:**
```python
def init_ui(self):
    """Initialize user interface."""

def create_widgets(self):
    """Create all UI widgets."""

def handle_process(self):
    """Handle Process button click event."""
```

#### Variables
- **Format:** `lowercase_with_underscores`
- **Descriptive names preferred over abbreviations**
- **Examples:**
  - `input_field` (not `inp_fld`)
  - `process_button` (not `proc_btn`)
  - `text_content` (not `txt`)

#### Constants
- **Format:** `UPPER_CASE_WITH_UNDERSCORES`
- **Examples:**
  - `WINDOW_WIDTH = 400`
  - `WINDOW_HEIGHT = 200`
  - `DEFAULT_TITLE = "Simple PyQt6 UI"`

#### Private Members
- **Format:** `_leading_underscore`
- **Use for internal implementation details**
- **Examples:**
  - `_internal_state`
  - `_helper_method()`

### Documentation Standards

#### Module Docstrings
Every Python file should start with a module docstring:

```python
"""
Simple PyQt6 UI Application Entry Point.

This module serves as the main entry point for the PyQt6 desktop application.
It initializes the QApplication and launches the main window.
"""
```

#### Class Docstrings
Every class must have a docstring:

```python
class MainWindow(QMainWindow):
    """
    Main application window with input field and action buttons.

    Provides a simple single-window interface demonstrating PyQt6
    event handling and layout management.
    """
```

#### Function/Method Docstrings
All public functions and methods must have docstrings:

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

**For complex functions, include Args and Returns:**

```python
def validate_input(self, text: str) -> bool:
    """
    Validate input text against defined rules.

    Args:
        text: The input text to validate

    Returns:
        bool: True if valid, False otherwise
    """
```

#### Inline Comments
- Use inline comments sparingly for non-obvious logic
- Place comments on separate line above code (not inline)
- Use complete sentences with proper capitalization and punctuation

```python
# Good - explains why, not what
# Calculate character count excluding whitespace
char_count = len(text.replace(" ", ""))

# Bad - states the obvious
# Get the text from input field
text = self.input_field.text()
```

### Import Organization

Organize imports in three groups with blank line separation:

```python
# Standard library imports
import sys
from datetime import datetime

# Third-party imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtCore import Qt

# Local application imports
from ui.main_window import MainWindow
from config import settings
```

**Within each group:**
- Sort alphabetically
- Use absolute imports, not relative
- One import per line (except multiple items from same module)

### Code Structure Standards

#### Class Structure Order
Organize class members in this order:

1. Class variables
2. `__init__` method
3. Special methods (`__str__`, `__repr__`, etc.)
4. Public methods (alphabetically or logically grouped)
5. Private methods (alphabetically or logically grouped)

```python
class MainWindow(QMainWindow):
    """Main application window."""

    # 1. Class variables
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 200

    # 2. Initialization
    def __init__(self):
        super().__init__()
        self.init_ui()

    # 3. Public methods (grouped logically)
    def init_ui(self):
        """Initialize UI."""

    def create_widgets(self):
        """Create widgets."""

    # 4. Event handlers
    def handle_process(self):
        """Handle process event."""

    # 5. Private methods
    def _validate_state(self):
        """Validate internal state."""
```

#### Method Length
- Prefer short, focused methods (< 20 lines)
- Extract complex logic into helper methods
- One responsibility per method

#### Line Breaks
- Break long lines at logical points
- Use parentheses for implicit line continuation

```python
# Good
widget_list = [
    self.process_btn,
    self.validate_btn,
    self.clear_btn
]

# Good
result = some_function(
    parameter1,
    parameter2,
    parameter3
)
```

## Markdown Documentation Standards

### Frontmatter
All documentation markdown files MUST include YAML frontmatter:

```yaml
---
name: document-name
created: 2025-12-19T01:40:55Z
updated: 2025-12-19T01:40:55Z
status: active
---
```

**Required fields:**
- `created` - ISO 8601 datetime (never change after creation)
- `updated` - ISO 8601 datetime (update on every modification)

**Common optional fields:**
- `name` - Document identifier
- `status` - Document state (active, completed, archived)
- `version` - Version number
- `author` - Creator or system name

### File Naming
- **Format:** `kebab-case.md`
- **Examples:**
  - `project-overview.md`
  - `tech-context.md`
  - `epic-pyqt6-ui.md`

### Heading Structure
- Use ATX-style headers (`#`, `##`, `###`)
- One H1 (`#`) per document (the title)
- Don't skip heading levels
- Use sentence case for headings

```markdown
# Main Title

## Section Title

### Subsection Title

#### Detail Level
```

### Lists
- Use `-` for unordered lists (consistent with markdown standard)
- Use `1.` for ordered lists (auto-numbering)
- Indent nested lists by 2 spaces

```markdown
- First item
  - Nested item
  - Another nested item
- Second item

1. First step
2. Second step
3. Third step
```

### Code Blocks
- Use triple backticks with language identifier
- Specify language for syntax highlighting

```markdown
\```python
def example():
    print("Hello, world!")
\```

\```bash
git commit -m "Example commit"
\```
```

### Emphasis
- Use `**bold**` for strong emphasis
- Use `*italic*` for mild emphasis
- Use `code` for inline code, commands, file names

### Links
- Use descriptive link text, not "click here"
- Format: `[Link Text](URL)`
- For internal references: Use relative paths

```markdown
# Good
See [tech context](./tech-context.md) for details.

# Bad
Click [here](./tech-context.md) for details.
```

## File Organization Standards

### Directory Structure
```
project/
├── main.py              # Entry point (minimal)
├── package/             # Main package
│   ├── __init__.py      # Package initialization
│   ├── module1.py       # Focused modules
│   └── module2.py
├── tests/               # Test files (when implemented)
│   └── test_module1.py
├── docs/                # Additional documentation
├── requirements.txt     # Dependencies
└── README.md           # User-facing docs
```

### Package Initialization
`__init__.py` files should be minimal:

```python
# Good - simple package marker
"""Package for UI components."""

# Avoid - complex initialization logic in __init__.py
```

## Git Commit Standards

### Commit Message Format
```
Issue #{number}: {Brief description}

{Optional detailed explanation}
{Optional additional context}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Examples:**
```
Issue #3: Create project structure and dependencies

Set up basic PyQt6 project with requirements.txt and README.
Created ui package directory for future UI components.
```

### Commit Frequency
- Commit early and often
- One logical change per commit
- Commit after completing each task
- Don't commit broken code to main branch

### What to Commit
- Source code
- Documentation
- Configuration files
- Requirements files

### What NOT to Commit
- Compiled files (`*.pyc`, `__pycache__`)
- Virtual environments (`venv/`, `.venv/`)
- IDE settings (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Secrets or credentials

## Testing Standards (Future)

### Test File Organization
```
tests/
├── __init__.py
├── test_main_window.py
├── test_handlers.py
└── test_validation.py
```

### Test Naming
- **Files:** `test_{module_name}.py`
- **Classes:** `Test{ClassName}`
- **Methods:** `test_{what_is_tested}`

```python
class TestMainWindow:
    def test_window_initialization(self):
        """Test that window initializes correctly."""

    def test_process_button_click(self):
        """Test process button event handler."""
```

### Test Documentation
- Every test method has a docstring
- Docstring explains what is being tested and expected outcome

## Error Handling Standards

### Exception Handling
- Catch specific exceptions, not generic `Exception`
- Log errors with context
- Provide user-friendly error messages

```python
# Good
try:
    result = risky_operation()
except FileNotFoundError as e:
    print(f"[Error] File not found: {e.filename}")
except PermissionError:
    print("[Error] Permission denied. Check file permissions.")

# Bad
try:
    result = risky_operation()
except:
    pass  # Silent failure
```

### Error Messages
- Start with context: `[Error]`, `[Warning]`, `[Info]`
- Be specific about what failed
- Suggest how to fix the issue

```python
# Good
print("[Error] Cannot connect to database. Check connection string.")

# Bad
print("Error")
```

## Console Output Standards

### Structured Output Format
Use consistent prefixes for different message types:

```python
print(f"[Process] {message}")     # Action/process
print(f"[Validate] {message}")    # Validation
print(f"[Error] {message}")       # Error
print(f"[Warning] {message}")     # Warning
print(f"[Info] {message}")        # Information
print(f" {message}")             # Success (with emoji)
```

### Success/Failure Indicators
```python
print("[Validate] ✓ Valid - Input is correct")      # Success
print("[Validate] ✗ Invalid - Input is empty")      # Failure
print("[Validate] ⓘ Input contains special chars")  # Info
```

## Configuration Standards

### requirements.txt Format
```
# Production dependencies
PyQt6>=6.0.0

# Development dependencies (when added)
# pytest>=7.0.0
# black>=22.0.0
# pylint>=2.15.0
```

**Principles:**
- Pin major versions, allow minor/patch updates
- Group dependencies by purpose
- Comment optional or development dependencies
- Keep minimal—only include what's needed

## Code Review Checklist

Before committing code, verify:

**Python Code:**
- [ ] PEP 8 compliant (run linter)
- [ ] All public classes/methods have docstrings
- [ ] No commented-out code
- [ ] No debug print statements (unless intentional)
- [ ] Imports organized correctly
- [ ] No unused imports or variables
- [ ] Naming conventions followed

**Documentation:**
- [ ] README updated if user-facing changes
- [ ] Frontmatter updated with current datetime
- [ ] Code comments explain why, not what
- [ ] Links are valid
- [ ] Markdown properly formatted

**Git:**
- [ ] Commit message follows format
- [ ] One logical change per commit
- [ ] No sensitive data in commit
- [ ] Tests pass (when implemented)

## Tools and Automation

### Recommended Tools
- **Code Formatting:** `black` (when implemented)
- **Linting:** `pylint` or `flake8`
- **Type Checking:** `mypy` (optional)
- **Documentation:** `pydocstyle` for docstring validation

### Editor Configuration
Recommended settings for consistent formatting:

```json
{
  "editor.rulers": [79],
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

## Exceptions and Special Cases

### When to Deviate from Standards
- External library conventions (follow library's style)
- Performance-critical code (document deviations)
- Backward compatibility (with comment explaining why)

**Always document exceptions:**
```python
# Deviation from PEP 8: Line length exceeds 79 chars
# Reason: Breaking this URL would make it non-clickable
DOCUMENTATION_URL = "https://very-long-url-that-cannot-be-broken.com/path/to/resource"
```

## Continuous Improvement

This style guide is a living document. Suggest improvements through:
- Pull requests with rationale
- Discussion in issues
- Real-world usage examples
- Community feedback

**Last Updated:** 2025-12-19
**Next Review:** Quarterly or as needed
