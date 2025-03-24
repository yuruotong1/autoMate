"""
System tray icon implementation
"""
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QAction

class StatusTrayIcon(QSystemTrayIcon):
    """System tray icon that displays application status"""
    
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.setToolTip("autoMate")
        
        # Create context menu
        self.menu = QMenu()
        self.show_action = QAction("Show Main Window")
        self.show_action.triggered.connect(self.show_main_window)
        self.menu_status = QAction("Status: Idle")
        self.menu_status.setEnabled(False)
        self.menu_task = QAction("Task: None")
        self.menu_task.setEnabled(False)
        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(QApplication.quit)
        
        self.menu.addAction(self.show_action)
        self.menu.addSeparator()
        self.menu.addAction(self.menu_status)
        self.menu.addAction(self.menu_task)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)
        
        self.setContextMenu(self.menu)
        
        # Connect signals
        self.activated.connect(self.icon_activated)
        
    def show_main_window(self):
        if self.parent:
            self.parent.showNormal()
            self.parent.activateWindow()
            
    def icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_main_window()
            
    def update_status(self, status_text):
        """Update status text in tray tooltip and menu"""
        # Truncate if too long for menu
        short_status = status_text[:50] + "..." if len(status_text) > 50 else status_text
        self.menu_status.setText(f"Status: {short_status}")
        
        # Show brief notification but don't disrupt automation
        # Only show notification for 500ms (very brief) to not interfere with visual automation
        self.showMessage("autoMate Status", status_text, QSystemTrayIcon.MessageIcon.Information, 500)
        
    def update_task(self, task_text):
        """Update task text in tray menu"""
        short_task = task_text[:50] + "..." if len(task_text) > 50 else task_text
        self.menu_task.setText(f"Task: {short_task}") 