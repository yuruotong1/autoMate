"""
Main entry point for autoMate application
"""
import sys
import argparse
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="PyQt6 App")
    parser.add_argument("--windows_host_url", type=str, default='localhost:8006')
    parser.add_argument("--omniparser_server_url", type=str, default="localhost:8000")
    return parser.parse_args()

def main():
    """Main application entry point"""
    args = parse_arguments()
    app = QApplication(sys.argv)
    window = MainWindow(args)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 