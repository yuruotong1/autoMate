"""
Recording manager for autoMate
Handles recording and demonstration functionality
"""
from util.auto_control import AutoControl
from ui.recording_panel import RecordingIndicator
from ui.demonstration_panel import DemonstrationPanel
from PyQt6.QtCore import QThread, pyqtSignal
import time

class ActionListenThread(QThread):
    finished_signal = pyqtSignal() 
    
    def __init__(self, action_listen):
        super().__init__()
        self.action_listen = action_listen
    
    def run(self):
        try:
            # start listen
            self.action_listen.start_listen()
            
            # wait for interruption request
            while not self.isInterruptionRequested():
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Action listening error: {e}")
        finally:
            # stop listen and clean up resources
            try:
                self.action_listen.stop_listen()
                self.finished_signal.emit()
            except Exception as e:
                print(f"Cleanup error: {e}")
    
class RecordingManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.recording_in_progress = False
        self.recording_indicator = None
        self.demo_panel = None
        self.demonstration_mode = False
        self.action_listen = AutoControl()
    
    def start_demonstration(self):
        """Start demonstration mode for system learning"""
        # Set demonstration mode flag
        self.demonstration_mode = True
        
        # hide main window
        if self.parent:
            self.parent.showMinimized()
        
        # create and show independent demonstration control panel
        self.demo_panel = DemonstrationPanel(stop_callback=self.stop_demonstration)
        self.demo_panel.show()
        
        # create and start listen thread
        self.listen_thread = ActionListenThread(self.action_listen)
        self.listen_thread.finished_signal.connect(self.process_recorded_actions)
        self.listen_thread.start()
    
    def stop_demonstration(self):
        """Stop demonstration mode and process the recorded actions"""
        # stop listening to user actions
        self.listen_thread.requestInterruption()
        # close independent demonstration control panel
        if self.demo_panel:
            self.demo_panel.close()
            self.demo_panel = None
        
        # restore main window
        if self.parent:
            self.parent.showNormal()
        
        # Reset state
        self.demonstration_mode = False
    
    def process_recorded_actions(self):
        """process all recorded actions"""
        # get all collected actions
        recorded_actions = self.action_listen.auto_list
        print("recorded_actions: ", recorded_actions)
