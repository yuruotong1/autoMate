"""
Theme definitions and theme handling functionality
"""

# Theme definitions
THEMES = {
    "Light": {
        "main_bg": "#F5F5F5",
        "widget_bg": "#FFFFFF",
        "text": "#333333",
        "accent": "#4A86E8",
        "button_bg": "#E3E3E3",
        "button_text": "#333333",
        "border": "#CCCCCC",
        "selection_bg": "#D0E2F4"
    },
    "Dark": {
        "main_bg": "#2D2D2D",
        "widget_bg": "#3D3D3D",
        "text": "#FFFFFF",
        "accent": "#4A86E8",
        "button_bg": "#555555",
        "button_text": "#FFFFFF",
        "border": "#555555",
        "selection_bg": "#3A5F8A"
    }
}

def apply_theme(widget, theme_name="Light"):
    """Apply the specified theme to the widget"""
    theme = THEMES[theme_name]
    
    # Create stylesheet for the application
    stylesheet = f"""
    QMainWindow, QDialog {{
        background-color: {theme['main_bg']};
        color: {theme['text']};
    }}
    
    QWidget {{
        background-color: {theme['main_bg']};
        color: {theme['text']};
    }}
    
    QLabel {{
        color: {theme['text']};
    }}
    
    QPushButton {{
        background-color: {theme['button_bg']};
        color: {theme['button_text']};
        border: 1px solid {theme['border']};
        border-radius: 4px;
        padding: 5px 10px;
    }}
    
    QPushButton:hover {{
        background-color: {theme['accent']};
        color: white;
    }}
    
    QLineEdit, QTextEdit, QTableWidget, QComboBox {{
        background-color: {theme['widget_bg']};
        color: {theme['text']};
        border: 1px solid {theme['border']};
        border-radius: 4px;
        padding: 4px;
    }}
    
    QTextEdit {{
        background-color: {theme['widget_bg']};
    }}
    
    QTableWidget::item:selected {{
        background-color: {theme['selection_bg']};
    }}
    
    QHeaderView::section {{
        background-color: {theme['button_bg']};
        color: {theme['button_text']};
        padding: 4px;
        border: 1px solid {theme['border']};
    }}
    
    QSplitter::handle {{
        background-color: {theme['border']};
    }}
    
    QScrollBar {{
        background-color: {theme['widget_bg']};
    }}
    
    QScrollBar::handle {{
        background-color: {theme['button_bg']};
        border-radius: 4px;
    }}
    """
    
    widget.setStyleSheet(stylesheet) 