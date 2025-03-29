"""
Voice recording and speech-to-text module
"""
import time
import threading
import numpy as np
import pyaudio
import wave
import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
import webrtcvad
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from aip import AipSpeech


class VoiceRecorder(QObject):
    """
    Records audio and performs speech-to-text conversion
    Uses WebRTC VAD for voice activity detection
    """
    utterance_detected = pyqtSignal(dict)
    recording_finished = pyqtSignal()
    
    def __init__(self, sample_rate=16000, chunk_size=320, vad_mode=3):
        """
        Initialize the voice recorder
        
        Args:
            sample_rate: Audio sample rate (WebRTC VAD only supports 8000, 16000, 32000, 48000 Hz)
            chunk_size: Audio chunk size (WebRTC VAD requires 10, 20, or 30 ms chunks)
            vad_mode: WebRTC VAD aggressiveness mode (0-3)
        """
        super().__init__()
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size  # 20ms at 16kHz
        self.format = pyaudio.paInt16
        self.channels = 1
        
        # WebRTC Voice Activity Detection
        self.vad = webrtcvad.Vad(vad_mode)
        
        # Audio recording variables
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Adjust based on environment
        self.offline_mode = False
        self.speech_counter = 0
        
        # Control flags
        self.is_recording = False
        self.recording_thread = None
        
        # Create app temp directory
        self.temp_dir = os.path.join(tempfile.gettempdir(), "automate_voice")
        os.makedirs(self.temp_dir, exist_ok=True)
        print(f"Using temp directory: {self.temp_dir}")
        
        # 从环境变量中加载百度语音API凭证
        app_id = os.environ.get('BAIDU_APP_ID')
        api_key = os.environ.get('BAIDU_API_KEY')
        secret_key = os.environ.get('BAIDU_SECRET_KEY')
        
        if app_id and api_key and secret_key:
            self.baidu_client = AipSpeech(app_id, api_key, secret_key)
            print("Baidu speech recognition initialized")
        else:
            print("Warning: Baidu API credentials not found in environment variables")
            print("Please set BAIDU_APP_ID, BAIDU_API_KEY, and BAIDU_SECRET_KEY")
            self.baidu_client = None
            self.offline_mode = True
        
    def start_recording(self):
        """Start audio recording in a separate thread"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.frames = []
        self.speech_counter = 0
        
        try:
            # Open audio stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            # Start recording thread
            self.recording_thread = threading.Thread(target=self._record)
            self.recording_thread.daemon = True
            self.recording_thread.start()
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.is_recording = False
        
    def _record(self):
        """Recording process that detects speech and performs STT"""
        # Variables for speech detection
        speech_frames = []
        silence_counter = 0
        speech_detected = False
        speech_end_time = 0
        
        try:
            while self.is_recording:
                # Read audio chunk
                audio_chunk = self.stream.read(self.chunk_size, exception_on_overflow=False)
                self.frames.append(audio_chunk)
                
                # Check for voice activity
                try:
                    is_speech = self.vad.is_speech(audio_chunk, self.sample_rate)
                except Exception as e:
                    print(f"VAD error: {e}")
                    is_speech = False
                
                if is_speech:
                    # Reset silence counter when speech is detected
                    silence_counter = 0
                    
                    if not speech_detected:
                        # Mark beginning of speech
                        speech_detected = True
                        speech_frames = []
                    
                    # Collect speech frames
                    speech_frames.append(audio_chunk)
                else:
                    if speech_detected:
                        silence_counter += 1
                        speech_frames.append(audio_chunk)
                        
                        # Consider speech ended after 1.5 seconds of silence (75 frames at 20ms per frame)
                        if silence_counter > 75:
                            speech_detected = False
                            silence_counter = 0
                            speech_end_time = time.time()
                            
                            # Process the speech for transcription
                            self._process_speech(speech_frames)
                            speech_frames = []
        except Exception as e:
            print(f"Recording error: {e}")
        finally:
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except Exception as e:
                    print(f"Error closing stream: {e}")
    
    def _process_speech(self, speech_frames):
        """
        Process recorded speech frames to extract text
        
        Args:
            speech_frames: List of audio frames containing speech
        """
        if not speech_frames:
            return
        
        self.speech_counter += 1
        # Save speech to temporary WAV file
        temp_file = os.path.join(self.temp_dir, f"speech_{self.speech_counter}.wav")
        
        try:
            wf = wave.open(temp_file, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(speech_frames))
            wf.close()
            
            # Convert to AudioSegment for potential preprocessing
            audio_segment = AudioSegment.from_wav(temp_file)
            
            if not self.offline_mode and self.baidu_client:
                try:
                    # 使用百度语音识别
                    with open(temp_file, 'rb') as f:
                        audio_data = f.read()
                    
                    # 调用百度语音API进行识别
                    result = self.baidu_client.asr(audio_data, 'wav', self.sample_rate, {
                        'dev_pid': 1537,  # 普通话(有标点)
                    })
                    
                    if result['err_no'] == 0:
                        text = result['result'][0]
                        print(f"Recognized text: {text}")
                    else:
                        print(f"Baidu ASR error: {result['err_msg']}")
                        raise Exception(f"Baidu ASR error: {result['err_msg']}")
                        
                except (Exception, ConnectionError) as e:
                    print(f"Online speech recognition failed: {e}")
                    print("Switching to offline mode")
                    self.offline_mode = True
                    text = self._offline_speech_recognition(temp_file)
            else:
                # Offline mode or no Baidu client
                text = self._offline_speech_recognition(temp_file)
                
            if text:
                # Emit the detected utterance with timestamp
                self.utterance_detected.emit({
                    "type": "utterance",
                    "timestamp": time.time(),
                    "text": text
                })
        except Exception as e:
            print(f"Speech recognition error: {e}")
            # Still emit an utterance with placeholder text in case of error
            self.utterance_detected.emit({
                "type": "utterance",
                "timestamp": time.time(),
                "text": f"[语音识别失败 #{self.speech_counter}]"
            })
    
    def _offline_speech_recognition(self, audio_file):
        """
        Perform offline speech recognition (fallback when online fails)
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            str: Recognized text or empty string
        """
        # For now, we'll just use a placeholder text since we don't have a real offline STT engine
        # In a real implementation, you'd use something like Vosk or Whisper for offline recognition
        return f"语音识别离线模式 #{self.speech_counter}"
    
    def stop_recording(self):
        """Stop the audio recording"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)
            
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            except Exception as e:
                print(f"Error stopping recording: {e}")
            
        self.recording_finished.emit()
        
    def save_recording(self, filename):
        """
        Save the full recording to a WAV file
        
        Args:
            filename: Output filename
        """
        if not self.frames:
            return False
            
        try:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            return True
        except Exception as e:
            print(f"Error saving recording: {e}")
            return False
        
    def __del__(self):
        """Clean up resources"""
        self.stop_recording()
        try:
            self.audio.terminate()
        except Exception:
            pass 