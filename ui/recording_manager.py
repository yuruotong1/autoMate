"""
Recording manager for autoMate
Handles recording and demonstration functionality
"""
import util.auto_control as auto_control
from ui.recording_panel import RecordingIndicator
from ui.demonstration_panel import DemonstrationPanel

class RecordingManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.recording_in_progress = False
        self.recording_indicator = None
        self.demo_panel = None
        self.demonstration_mode = False
        
    def start_recording(self):
        """Start recording user actions"""
        if not self.recording_in_progress:
            self.recording_in_progress = True
            
            # 最小化主窗口
            if self.parent:
                self.parent.showMinimized()
            
            # 显示录制指示器
            self.recording_indicator = RecordingIndicator(stop_callback=self.stop_recording)
            self.recording_indicator.show()
            
            # 开始监听用户动作
            auto_control.start_monitoring()
            
    def stop_recording(self):
        """Stop recording user actions"""
        if self.recording_in_progress:
            self.recording_in_progress = False
            
            # 停止监听用户动作
            auto_control.stop_monitoring()
            
            # 关闭录制指示器
            if self.recording_indicator:
                self.recording_indicator.close()
                self.recording_indicator = None
            
            # 恢复主窗口
            if self.parent:
                self.parent.showNormal()
    
    def start_demonstration(self):
        """Start demonstration mode for system learning"""
        # Set demonstration mode flag
        self.demonstration_mode = True
        
        # 隐藏主窗口
        if self.parent:
            self.parent.showMinimized()
        
        # 创建并显示独立的演示控制面板
        self.demo_panel = DemonstrationPanel(stop_callback=self.stop_demonstration)
        self.demo_panel.show()
        
        # 开始监听用户动作
        auto_control.start_monitoring()
    
    def stop_demonstration(self):
        """Stop demonstration mode and process the recorded actions"""
        # 停止监听用户动作
        auto_control.stop_monitoring()
        
        # 关闭独立的演示控制面板
        if self.demo_panel:
            self.demo_panel.close()
            self.demo_panel = None
        
        # 恢复主窗口
        if self.parent:
            self.parent.showNormal()
        
        # Reset state
        self.demonstration_mode = False 