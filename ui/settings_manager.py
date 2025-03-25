"""
Settings manager for autoMate
Handles loading, saving, and updating application settings
"""
from xbrain.utils.config import Config
from ui.hotkey_edit import DEFAULT_STOP_HOTKEY

class SettingsManager:
    """Manages application settings"""
    
    def __init__(self):
        self.config = Config()
        self.settings = self.load_initial_settings()
    
    def load_initial_settings(self):
        """Load initial settings from config"""
        return {
            "api_key": self.config.OPENAI_API_KEY or "",
            "base_url": self.config.OPENAI_BASE_URL or "https://api.openai.com/v1",
            "model": self.config.OPENAI_MODEL or "gpt-4o",
            "theme": "Light",
            "stop_hotkey": DEFAULT_STOP_HOTKEY,
            "only_n_most_recent_images": 2,
            "screen_region": None
        }
    
    def get_settings(self):
        """Get current settings"""
        return self.settings
    
    def update_settings(self, new_settings):
        """Update settings"""
        # Track if hotkey changed
        hotkey_changed = False
        if "stop_hotkey" in new_settings and new_settings["stop_hotkey"] != self.settings.get("stop_hotkey"):
            hotkey_changed = True
            
        # Track if theme changed
        theme_changed = False
        if "theme" in new_settings and new_settings["theme"] != self.settings.get("theme"):
            theme_changed = True
            
        # Update settings
        self.settings.update(new_settings)
        
        return {
            "hotkey_changed": hotkey_changed,
            "theme_changed": theme_changed
        }
    
    def save_to_config(self):
        """Save settings to config file"""
        # Update config with current settings
        self.config.OPENAI_API_KEY = self.settings.get("api_key", "")
        self.config.OPENAI_BASE_URL = self.settings.get("base_url", "https://api.openai.com/v1")
        self.config.OPENAI_MODEL = self.settings.get("model", "gpt-4o")
        
        # Save config to file
        self.config.save() 