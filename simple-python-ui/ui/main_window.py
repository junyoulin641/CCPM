"""
Main window implementation for Simple PyQt6 UI application.

This module contains the MainWindow class that defines the primary
user interface with input field, label, and action buttons.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Main application window with input field and action buttons."""

    def __init__(self):
        """Initialize window and call setup methods."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Configure window properties (title, size, central widget)."""
        # Set window properties
        self.setWindowTitle("Simple PyQt6 UI")
        self.setGeometry(100, 100, 400, 200)  # x, y, width, height

        # Create central widget and set it
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create widgets and setup layout
        self.create_widgets()
        self.setup_layout(central_widget)

    def create_widgets(self):
        """Instantiate all UI widgets."""
        # Create label for input field
        self.label = QLabel("Enter text:")

        # Create text input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something here...")

        # Create action buttons
        self.process_btn = QPushButton("Process")
        self.validate_btn = QPushButton("Validate")
        self.clear_btn = QPushButton("Clear")

    def setup_layout(self, central_widget):
        """Arrange widgets using layouts."""
        # Create main vertical layout with margins and spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # 10px margins
        main_layout.setSpacing(10)  # 10px spacing between widgets

        # Add label and input field to main layout
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.input_field)

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add stretch before buttons for center alignment
        button_layout.addWidget(self.process_btn)
        button_layout.addWidget(self.validate_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()  # Add stretch after buttons for center alignment

        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Add stretch at bottom to keep widgets at top
        main_layout.addStretch()

        # Set the layout on the central widget
        central_widget.setLayout(main_layout)
