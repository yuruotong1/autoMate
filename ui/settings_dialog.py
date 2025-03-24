"""
Settings dialog for application configuration
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                          QLabel, QLineEdit, QPushButton, QComboBox)
from PyQt6.QtCore import QTimer
from ui.hotkey_edit import HotkeyEdit, DEFAULT_STOP_HOTKEY
from ui.theme import THEMES

class SettingsDialog(QDialog):
    """Dialog for application settings"""
    
    def __init__(self, parent=None, state=None):
        super().__init__(parent)
        self.state = state
        self.parent_window = parent
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Model settings
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:")
        self.model_input = QLineEdit(self.state["model"])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_input)
        
        # Base URL settings
        url_layout = QHBoxLayout()
        url_label = QLabel("Base URL:")
        self.base_url_input = QLineEdit(self.state["base_url"])
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.base_url_input)
        
        # API key settings
        api_layout = QHBoxLayout()
        api_label = QLabel("API Key:")
        self.api_key_input = QLineEdit(self.state["api_key"])
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input)
        
        # Theme selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))
        current_theme = self.state.get("theme", "Light")
        self.theme_combo.setCurrentText(current_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        
        # Stop hotkey setting
        hotkey_layout = QHBoxLayout()
        hotkey_label = QLabel("Stop Hotkey:")
        self.hotkey_edit = HotkeyEdit(self.state.get("stop_hotkey", DEFAULT_STOP_HOTKEY))
        hotkey_layout.addWidget(hotkey_label)
        hotkey_layout.addWidget(self.hotkey_edit)
        
        # Screen region selection
        region_layout = QHBoxLayout()
        self.select_region_btn = QPushButton("Select Screen Region")
        self.region_info = QLabel("No region selected" if "screen_region" not in self.state else f"Selected region: {self.state['screen_region']}")
        self.select_region_btn.clicked.connect(self.select_screen_region)
        region_layout.addWidget(self.select_region_btn)
        region_layout.addWidget(self.region_info)
        
        # OK and Cancel buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        # Add all elements to main layout
        layout.addLayout(model_layout)
        layout.addLayout(url_layout)
        layout.addLayout(api_layout)
        layout.addLayout(theme_layout)
        layout.addLayout(hotkey_layout)
        layout.addLayout(region_layout)
        layout.addLayout(button_layout)
    
    def select_screen_region(self):
        """Select screen region"""
        # Minimize the parent window before selecting region
        if self.parent_window:
            self.parent_window.showMinimized()
            # Wait a moment for the window to minimize
            QTimer.singleShot(500, self._do_select_region)
        else:
            self._do_select_region()
            
    def _do_select_region(self):
        """Actual region selection after minimizing"""
        from util.screen_selector import ScreenSelector
        region = ScreenSelector().get_selection()
        
        # Restore the dialog and parent window
        self.activateWindow()
        if self.parent_window:
            self.parent_window.showNormal()
            self.parent_window.activateWindow()
        
        if region:
            self.state["screen_region"] = region
            self.region_info.setText(f"Selected region: {region}")
        else:
            self.region_info.setText("Selection cancelled")
    
    def get_settings(self):
        """Get settings content"""
        return {
            "model": self.model_input.text(),
            "base_url": self.base_url_input.text(),
            "api_key": self.api_key_input.text(),
            "screen_region": self.state.get("screen_region", None),
            "theme": self.theme_combo.currentText(),
            "stop_hotkey": self.hotkey_edit.get_hotkey()
        } 