"""
Main entry point for the AutoMate application
"""
import sys
from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def main():
    """
    Main application entry point
    
    Creates and runs the AutoMate application
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 