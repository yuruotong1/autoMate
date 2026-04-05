#!/usr/bin/env python3
"""
Entry point for autoMate PyQt6 GUI.

Run with: python pyqt_gui/main.py
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from gui.main_window import MainWindow


def main():
    """Initialize and run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("autoMate")
    app.setOrganizationName("autoMate")

    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    # Set dark fusion style
    app.setStyle("Fusion")

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
