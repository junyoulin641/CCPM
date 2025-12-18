"""
Simple PyQt6 UI Application Entry Point.

This module serves as the main entry point for the PyQt6 desktop application.
It initializes the QApplication and launches the main window.
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """
    Initialize and run the PyQt6 application.

    Creates a QApplication instance, instantiates the MainWindow,
    displays it, and starts the application event loop.

    Returns:
        int: Application exit code
    """
    # Create QApplication instance
    app = QApplication(sys.argv)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Start event loop and exit with proper code
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
