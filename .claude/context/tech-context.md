---
created: 2025-12-19T01:40:55Z
last_updated: 2025-12-19T01:40:55Z
version: 1.0
author: Claude Code PM System
---

# Technical Context

## Technology Stack

### Primary Languages
- **Python 3.8+** - Main application development language
- **Markdown** - Documentation and PM artifacts
- **Bash** - PM system automation scripts
- **YAML** - Frontmatter metadata and configuration

### GUI Framework
- **PyQt6 >= 6.0.0** - Python bindings for Qt 6 framework
  - QMainWindow - Application window management
  - QWidget - UI component base classes
  - QLayout - Layout management (QVBoxLayout, QHBoxLayout)
  - QPushButton, QLineEdit, QLabel - UI widgets

### Development Tools
- **Git** - Version control
- **GitHub CLI (gh)** - Issue tracking integration
- **Claude Code** - AI-powered development assistant
- **pip** - Python package management

## Dependencies

### Application Dependencies
**File:** `simple-python-ui/requirements.txt`
```
PyQt6>=6.0.0
```

**Why PyQt6:**
- Modern Qt 6 framework binding
- Active maintenance and support
- Comprehensive widget library
- Cross-platform compatibility (Windows, Linux, macOS)
- Pythonic API design

### System Dependencies
- **Python 3.8+** - Required for PyQt6 compatibility
- **Git 2.x** - Version control and PM system operations
- **GitHub CLI** - GitHub issue integration (optional but recommended)

### Development Dependencies
**None currently** - Minimal project setup without testing frameworks or build tools

### Future Dependency Considerations
- **pytest** - For automated testing
- **black** - Code formatting
- **pylint/flake8** - Code quality checks
- **PyInstaller** - For building standalone executables

## Development Environment

### Recommended Setup
- **Python Version:** 3.8 or higher
- **Virtual Environment:** Recommended (venv or virtualenv)
- **IDE/Editor:** Any Python-compatible editor (VS Code, PyCharm, etc.)
- **Terminal:** Command prompt, PowerShell, or bash
- **Git Client:** Command-line git or GUI client

### Installation Steps
```bash
# 1. Clone repository
git clone https://github.com/junyoulin641/CCPM.git
cd CCPM

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
cd simple-python-ui
pip install -r requirements.txt

# 4. Run application
python main.py
```

## Architecture Patterns

### PyQt6 Application Pattern
- **Single QMainWindow** - Main application window
- **Event-Driven Architecture** - Signal-slot connections for UI events
- **Layout-Based UI** - QVBoxLayout/QHBoxLayout instead of absolute positioning
- **Separation of Concerns:**
  - UI creation (create_widgets)
  - Layout setup (setup_layout)
  - Event handling (handle_* methods)
  - Signal connections (connect_signals)

### PM System Architecture
- **Command Pattern** - Slash commands in `.claude/commands/`
- **Agent Pattern** - Specialized agents for different tasks
- **Frontmatter Metadata** - YAML headers in markdown files
- **File-Based Storage** - Documentation in structured directories
- **GitHub Integration** - Bidirectional sync with GitHub Issues

## Code Quality Standards

### Python Standards
- **PEP 8 Compliance** - Python style guide adherence
- **Docstrings Required** - All classes and methods documented
- **Type Hints** - Recommended for function signatures (not yet implemented)
- **Naming Conventions:**
  - snake_case for functions/methods
  - PascalCase for classes
  - UPPER_CASE for constants

### Documentation Standards
- **Comprehensive README** - User-facing documentation
- **Inline Comments** - Explain non-obvious logic
- **Function Docstrings** - Purpose, parameters, returns
- **Class Docstrings** - Overall purpose and usage

## Testing Strategy

### Current Testing Approach
- **Manual Testing** - Primary QA method (Task #6)
- **Code Review** - Static analysis and inspection
- **Acceptance Criteria Verification** - Checklist-based validation

### Testing Coverage (Manual)
Documented in `doc/simple-python-ui/epics/basic-ui/.archived/epic-pyqt6-ui/updates/6/test-results.md`:
- Application launch tests
- Widget creation tests
- Event handler tests
- Layout verification tests
- Input validation tests
- Console output tests
- PEP 8 compliance tests
- Edge case handling tests

### Future Testing Plans
- **Unit Tests** - pytest for individual functions
- **Integration Tests** - End-to-end user workflows
- **UI Tests** - Automated PyQt6 testing (pytest-qt)
- **CI/CD** - GitHub Actions for automated testing

## Platform Compatibility

### Primary Platform
- **Windows** - Primary development and testing platform

### Target Platforms
- **Windows 10/11** - Fully supported
- **Linux** - Compatible (PyQt6 supports major distributions)
- **macOS** - Compatible (PyQt6 supports recent macOS versions)

### Platform-Specific Notes
- Line endings: CRLF on Windows, LF on Unix (git handles conversion)
- Paths: Use os.path or pathlib for cross-platform compatibility
- GUI: PyQt6 provides native look and feel on each platform

## Performance Considerations

### Application Performance
- **Launch Time:** < 2 seconds (target met)
- **Button Response:** < 100ms (instantaneous feel)
- **Memory Usage:** Minimal (single-window, no persistent data)
- **CPU Usage:** Low (event-driven, no background processing)

### Optimization Strategies
- Lazy loading of UI components (if needed in future)
- Efficient event handlers (no blocking operations)
- Clean shutdown (proper QApplication exit)

## Security Considerations

### Current Security Posture
- **No Network Access** - Standalone desktop application
- **No Data Persistence** - No sensitive data stored
- **No External Dependencies** - Minimal attack surface
- **Input Validation** - Basic alphanumeric validation implemented

### Future Security Enhancements
- Input sanitization for advanced features
- Secure file operations if persistence added
- Code signing for distribution
- Dependency vulnerability scanning

## Version Control

### Git Configuration
- **Repository:** https://github.com/junyoulin641/CCPM.git
- **Default Branch:** main
- **Branching Strategy:** Epic branches (epic/{name})
- **Merge Strategy:** No fast-forward merges (--no-ff)

### Commit Conventions
- Format: `Issue #{number}: {description}`
- Examples:
  - `Issue #3: Create project structure and dependencies`
  - `Issue #7: Complete documentation and code comments`
- Epic lifecycle commits:
  - Merge: `Merge epic: {name}`
  - Close: `Epic completion: Final status updates`
  - Archive: `Archive completed epic: {name}`

## Integration Points

### GitHub Integration
- **Issue Tracking** - Epics and tasks synced as GitHub Issues
- **Labels** - Feature/epic categorization
- **Parent-Child Links** - Epic and task relationships (gh-sub-issue extension)
- **Status Sync** - Local file status synced to GitHub

### Claude Code Integration
- **PM Commands** - 20+ slash commands for project management
- **Agents** - Specialized AI agents for tasks
- **Context System** - Project context documentation
- **Skills** - Reusable capabilities (code-style)

## Future Technology Considerations

### Potential Additions
- **Database** - SQLite for data persistence
- **Configuration** - TOML or YAML config files
- **Logging** - Python logging framework
- **Testing** - pytest, pytest-qt
- **Packaging** - PyInstaller or cx_Freeze for executables
- **Documentation** - Sphinx for API documentation
