"""
Recorder manager module for coordinating input and voice recording
"""
import os
import time
import json
import traceback
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer

from src.core.input_listener import InputListener
from src.core.voice_recorder import VoiceRecorder


class RecorderManager(QObject):
    """
    Manages and coordinates the recording of user inputs (keyboard/mouse)
    and voice data, producing a synchronized mixed sequence
    """
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal()
    sequence_updated = pyqtSignal(list)
    status_changed = pyqtSignal(str)
    
    def __init__(self):
        """Initialize recorder manager"""
        super().__init__()
        
        # Store the sequence
        self.mixed_sequence = []
        self.is_recording = False
        
        # Create input listener
        self.input_listener = InputListener()
        self.input_listener.action_detected.connect(self.on_action_detected)
        
        try:
            # Create voice recorder
            self.voice_recorder = VoiceRecorder()
            self.voice_recorder.utterance_detected.connect(self.on_utterance_detected)
            self.has_voice_recorder = True
        except Exception as e:
            self.status_changed.emit(f'警告：无法初始化语音录制器，将只记录键盘鼠标事件: {str(e)}')
            print(f"Error initializing voice recorder: {e}")
            traceback.print_exc()
            self.has_voice_recorder = False
        
    @pyqtSlot()
    def start_recording(self):
        """Start recording both inputs and voice"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.mixed_sequence = []
        
        # Start input listener
        try:
            self.input_listener.start_listen()
        except Exception as e:
            self.status_changed.emit(f'启动输入监听失败: {str(e)}')
            print(f"Error starting input listener: {e}")
        
        # Start voice recorder if available
        if self.has_voice_recorder:
            try:
                self.voice_recorder.start_recording()
            except Exception as e:
                self.status_changed.emit(f'启动语音录制失败: {str(e)}')
                print(f"Error starting voice recorder: {e}")
        
        self.recording_started.emit()
        
    @pyqtSlot()
    def stop_recording(self):
        """Stop all recording activities"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        # Stop input listener
        try:
            self.input_listener.stop_listen()
        except Exception as e:
            print(f"Error stopping input listener: {e}")
        
        # Stop voice recorder if available
        if self.has_voice_recorder:
            try:
                self.voice_recorder.stop_recording()
            except Exception as e:
                print(f"Error stopping voice recorder: {e}")
        
        self.recording_stopped.emit()
        
    @pyqtSlot(dict)
    def on_action_detected(self, action_data):
        """
        Handle detected input actions
        
        Args:
            action_data: Dictionary containing action details
        """
        if not self.is_recording:
            return
            
        # Format into mixed sequence entry
        action_entry = {
            "type": "action",
            "timestamp": time.time(),
            "event": action_data["event"]
        }
        
        # Add position for mouse events
        if action_data.get("position"):
            action_entry["position"] = action_data["position"]
            
        # Extract target information (would need additional image processing)
        # For now, we're just storing the raw event data
        action_entry["screenshot"] = action_data.get("base64_image", "")
        
        # Add to sequence
        self.mixed_sequence.append(action_entry)
        self.sequence_updated.emit(self.mixed_sequence)
        
    @pyqtSlot(dict)
    def on_utterance_detected(self, utterance_data):
        """
        Handle detected utterances
        
        Args:
            utterance_data: Dictionary containing utterance details
        """
        if not self.is_recording:
            return
            
        # Add to sequence
        self.mixed_sequence.append(utterance_data)
        self.sequence_updated.emit(self.mixed_sequence)
        self.status_changed.emit(f'已检测到语音: {utterance_data.get("text", "")}')
    
    def save_sequence(self, filename):
        """
        Save the recorded mixed sequence to a JSON file
        
        Args:
            filename: Output filename
        
        Returns:
            bool: True if saved successfully
        """
        if not self.mixed_sequence:
            return False
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.mixed_sequence, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving sequence: {e}")
            return False
    
    def load_sequence(self, filename):
        """
        Load a previously saved mixed sequence
        
        Args:
            filename: Input filename
            
        Returns:
            bool: True if loaded successfully
        """
        if not os.path.exists(filename):
            return False
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.mixed_sequence = json.load(f)
            self.sequence_updated.emit(self.mixed_sequence)
            return True
        except Exception as e:
            print(f"Error loading sequence: {e}")
            return False
    
    def get_workflow_segments(self):
        """
        Extract workflow segments from the mixed sequence
        
        Returns:
            List of (utterance, actions) pairs
        """
        from src.core.workflow_extractor import WorkflowExtractor
        
        extractor = WorkflowExtractor()
        return extractor.extract_workflows(self.mixed_sequence) 