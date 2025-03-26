"""
Main entry point for the AutoMate application
"""
import sys
from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from xbrain.utils.config import Config


def main():
    """
    Main application entry point
    
    Creates and runs the AutoMate application
    """
    config = Config()
    base_url = "https://api.openai-next.com/v1"
    api_key = "sk-fb4R0ieuTV2OISKX715e7e4a588447F0A6A0AaE6123d16C7"
    model = "gpt-4o"
    config.set_openai_config(base_url=base_url, api_key=api_key, model=model)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 