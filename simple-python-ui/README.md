# Simple PyQt6 UI

A minimal PyQt6 desktop application that serves as a starter template and learning tool for PyQt6 GUI development. Features a clean single-window interface with text input and interactive buttons demonstrating basic event handling and console output.

## Features

- **Single-window interface** with QMainWindow
- **Text input field** for user text entry
- **Interactive buttons** with three actions:
  - **Process**: Transforms input text (uppercase, character count, reverse)
  - **Validate**: Checks if input is non-empty and alphanumeric
  - **Clear**: Resets the input field
- **Console feedback** for all button actions
- **Clean layout** using QVBoxLayout and QHBoxLayout
- **PEP 8 compliant** code with comprehensive docstrings

## Requirements

- **Python 3.8** or higher
- **PyQt6** (>= 6.0.0)

## Installation

1. **Clone or download** the repository

2. **Navigate to the project directory:**
   ```bash
   cd simple-python-ui
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

Launch the application from the command line:

```bash
python main.py
```

The application window will appear with the title "Simple PyQt6 UI" (400x200 pixels).

### Using the Application

1. **Enter text** in the input field (labeled "Enter text:")
2. **Click "Process"** to see text transformations:
   - Original text printed to console
   - Text converted to uppercase
   - Character count displayed
   - Text reversed
3. **Click "Validate"** to check input:
   - Validates if input is non-empty
   - Checks if input is alphanumeric
   - Provides success (✓) or failure (✗) feedback
4. **Click "Clear"** to reset the input field

### Expected Console Output

**Process Button Example:**
```
[Process] Original text: 'Hello World'
[Process] Uppercase: 'HELLO WORLD'
[Process] Character count: 11
[Process] Reversed: 'dlroW olleH'
```

**Validate Button Example (Valid):**
```
[Validate] Validating input...
[Validate] ✓ Valid - Input contains 5 character(s)
[Validate] Text: 'Hello'
[Validate] ⓘ Input contains special characters or spaces
```

**Validate Button Example (Invalid):**
```
[Validate] Validating input...
[Validate] ✗ Invalid - Input is empty
[Validate] Please enter some text
```

**Clear Button Example:**
```
[Clear] Input field cleared
```

## Project Structure

```
simple-python-ui/
├── main.py              # Application entry point - initializes QApplication
├── ui/
│   ├── __init__.py      # Makes ui a Python package
│   └── main_window.py   # MainWindow class with UI widgets and event handlers
├── requirements.txt     # Python dependencies (PyQt6>=6.0.0)
└── README.md           # This file - project documentation
```

### File Descriptions

- **main.py**: Entry point that creates QApplication, instantiates MainWindow, and starts the event loop
- **ui/main_window.py**: Contains the MainWindow class with:
  - Widget creation (QLabel, QLineEdit, QPushButton)
  - Layout setup (QVBoxLayout, QHBoxLayout)
  - Event handlers (handle_process, handle_validate, handle_clear)
  - Signal connections linking buttons to handlers
- **requirements.txt**: Specifies PyQt6 dependency for easy installation

## Troubleshooting

### Common Issues and Solutions

**Problem: ModuleNotFoundError: No module named 'PyQt6'**
```
Solution: Install PyQt6 using pip:
  pip install PyQt6
```

**Problem: Application doesn't launch / No window appears**
```
Solutions:
  1. Verify Python version is 3.8+:
     python --version
  2. Check for error messages in console
  3. Ensure you're in the correct directory:
     cd simple-python-ui
     python main.py
```

**Problem: Import errors from ui module**
```
Solution: Ensure __init__.py exists in ui/ directory and you're running from the project root:
  python main.py  (not: python ui/main.py)
```

**Problem: Window appears but buttons don't respond**
```
Solution: This indicates signal connections may be missing. Verify connect_signals() is called in MainWindow.__init__()
```

**Problem: Console output not visible**
```
Solution: Run the application from a terminal/command prompt window, not by double-clicking the file
```

## Extending the Application

### For Developers

This application is designed as a learning template. Here are some ideas for extending it:

**1. Add More Event Handlers:**
- Create new button widgets
- Implement additional text transformations (capitalize, count vowels, etc.)
- Add keyboard shortcuts (e.g., Ctrl+P for Process, Ctrl+C for Clear)

**2. Enhance UI:**
- Add a QTextEdit for multi-line output
- Create a status bar for feedback instead of console
- Add icons to buttons
- Implement themes or styles

**3. Add Persistence:**
- Save/load text to/from files
- Store recent inputs in a history list
- Add preferences/settings

**4. Improve Validation:**
- Add regex pattern matching
- Implement custom validation rules
- Show validation errors in GUI (QMessageBox)

### Code Structure

The code follows a clear separation of concerns:
- **UI creation** (create_widgets, setup_layout)
- **Event handling** (handle_process, handle_validate, handle_clear)
- **Signal connections** (connect_signals)

All methods include docstrings explaining their purpose, parameters, and behavior.

## Learning Resources

- **PyQt6 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Qt Documentation**: https://doc.qt.io/qt-6/
- **Python PEP 8 Style Guide**: https://peps.python.org/pep-0008/

## License

This project is provided as-is for educational purposes. Feel free to use, modify, and distribute as needed.

## Contributing

This is a learning template project. Feel free to fork and modify for your own use. Suggestions and improvements are welcome.

---

**Created with:** Python 3.8+, PyQt6
**Purpose:** Educational starter template for PyQt6 desktop applications
