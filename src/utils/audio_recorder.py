"""
Audio recording and speech recognition module
"""
import os
import time
import wave
import threading
import tempfile
import queue
import numpy as np
import pyaudio
import webrtcvad
import speech_recognition as sr
from PyQt6.QtCore import QObject, pyqtSignal
from aip import AipSpeech

class AudioRecorder(QObject):
    """
    Class for recording audio and performing speech recognition
    Emits signals when utterances are detected
    """
    utterance_detected = pyqtSignal(dict)
    recording_status = pyqtSignal(str)
    terminated = pyqtSignal()

    def __init__(self, vad_level=3, sample_rate=16000, chunk_duration_ms=30):
        """
        Initialize audio recorder with VAD and ASR
        
        Args:
            vad_level: VAD aggressiveness (0-3)
            sample_rate: Audio sample rate (Hz)
            chunk_duration_ms: Chunk duration (ms)
        """
        super().__init__()
        self.sample_rate = sample_rate
        self.chunk_duration_ms = chunk_duration_ms
        self.chunk_size = int(self.sample_rate * self.chunk_duration_ms / 1000)
        self.vad = webrtcvad.Vad(vad_level)
        
        # Audio recording setup
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.recording = False
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Adjust based on environment
        
        # Threading objects
        self.recording_thread = None
        self.transcription_thread = None
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        # Temporary directories for audio files
        self.temp_dir = tempfile.mkdtemp()
        self.current_audio_file = None
        self.active_audio_file = None
        
        # 初始化百度语音客户端
        app_id = os.environ.get('BAIDU_APP_ID')
        api_key = os.environ.get('BAIDU_API_KEY')
        secret_key = os.environ.get('BAIDU_SECRET_KEY')
        
        if app_id and api_key and secret_key:
            self.baidu_client = AipSpeech(app_id, api_key, secret_key)
            print("AudioRecorder: Baidu speech recognition initialized")
            self.use_baidu = True
        else:
            print("AudioRecorder: Warning - Baidu API credentials not found in environment variables")
            self.baidu_client = None
            self.use_baidu = False
        
    def _recording_worker(self):
        """Worker thread for audio recording with VAD"""
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        self.recording_status.emit("Ready for voice commands")
        
        # VAD state
        speech_frames = []
        is_speech = False
        silent_chunks = 0
        speech_chunks = 0
        max_silent_chunks = int(1000 / self.chunk_duration_ms)  # 1-second silence
        
        try:
            while not self.stop_event.is_set():
                audio_chunk = stream.read(self.chunk_size, exception_on_overflow=False)
                is_speech_frame = self.vad.is_speech(audio_chunk, self.sample_rate)
                
                # State machine for speech detection
                if is_speech_frame:
                    if not is_speech:
                        # Transition from silence to speech
                        is_speech = True
                        speech_frames = []  # Clear previous frames
                        self.recording_status.emit("Listening...")
                    
                    speech_chunks += 1
                    speech_frames.append(audio_chunk)
                else:
                    if is_speech:
                        # We are in speech state but got silence frame
                        silent_chunks += 1
                        
                        if silent_chunks > max_silent_chunks:
                            # End of speech
                            is_speech = False
                            silent_chunks = 0
                            speech_chunks = 0
                            
                            if len(speech_frames) > 15:  # Filter out very short sounds
                                timestamp = time.time()
                                audio_file = os.path.join(self.temp_dir, f"speech_{timestamp}.wav")
                                self._save_audio(audio_file, speech_frames)
                                self.audio_queue.put((audio_file, timestamp))
                                self.recording_status.emit("Processing speech...")
                    else:
                        # We're in silence state, just accumulating silence
                        pass
                    
                    # Still collect speech frames for a bit after speech ends
                    if silent_chunks < max_silent_chunks and is_speech:
                        speech_frames.append(audio_chunk)
        
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.terminated.emit()
    
    def _transcription_worker(self):
        """Worker thread for ASR"""
        while not self.stop_event.is_set():
            try:
                audio_file, timestamp = self.audio_queue.get(timeout=1)
                
                try:
                    with sr.AudioFile(audio_file) as source:
                        audio_data = self.recognizer.record(source)
                        # 从Google更改为百度语音识别
                        # text = self.recognizer.recognize_google(audio_data)
                        
                        # 将音频保存为临时文件以供百度API使用
                        temp_wav = os.path.join(tempfile.gettempdir(), "temp_speech.wav")
                        with wave.open(temp_wav, 'wb') as wf:
                            wf.setnchannels(1)
                            wf.setsampwidth(2)  # 16bit
                            wf.setframerate(16000)
                            wf.writeframes(audio_data.get_wav_data())
                            
                        # 读取文件并调用百度API
                        with open(temp_wav, 'rb') as f:
                            audio_bytes = f.read()
                            
                        # 调用百度语音API
                        result = self.baidu_client.asr(audio_bytes, 'wav', 16000, {
                            'dev_pid': 1537,  # Mandarin with punctuation
                        })
                        
                        if result['err_no'] == 0:
                            text = result['result'][0]
                        else:
                            raise Exception(f"Baidu ASR error: {result['err_msg']}")
                        
                        if text:
                            # Emit the utterance with timestamp
                            self.utterance_detected.emit({
                                "type": "utterance",
                                "timestamp": timestamp,
                                "text": text
                            })
                            self.recording_status.emit(f"Detected: \"{text}\"")
                
                except Exception as e:
                    print(f"Error recognizing speech: {e}")
                
                # Clean up temporary audio file
                try:
                    os.remove(audio_file)
                except (PermissionError, FileNotFoundError):
                    pass
                
                self.audio_queue.task_done()
            
            except queue.Empty:
                # Timeout, just continue
                pass
    
    def _save_audio(self, file_path, frames):
        """Save audio frames to WAV file"""
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
    
    def start_recording(self):
        """Start audio recording and speech recognition threads"""
        if self.recording:
            return
        
        self.recording = True
        self.stop_event.clear()
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self._recording_worker)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
        # Start transcription thread
        self.transcription_thread = threading.Thread(target=self._transcription_worker)
        self.transcription_thread.daemon = True
        self.transcription_thread.start()
    
    def stop_recording(self):
        """Stop all recording and transcription threads"""
        if not self.recording:
            return
        
        self.recording = False
        self.stop_event.set()
        
        # Wait for threads to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)
        
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.transcription_thread.join(timeout=2)
        
        self.terminated.emit()
        
    def __del__(self):
        """Cleanup temporary files on deletion"""
        self.stop_recording()
        
        # Clean up temp directory
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass
    
    def recognize_audio(self, audio_file_path=None, audio_data=None):
        """
        使用百度API进行语音识别
        """
        try:
            # 如果提供了音频数据，优先使用音频数据
            if audio_data is not None:
                if self.use_baidu and self.baidu_client:
                    # 使用百度API进行识别
                    result = self.baidu_client.asr(audio_data, 'pcm', 16000, {
                        'dev_pid': 1537,  # 普通话(有标点)
                    })
                    
                    if result['err_no'] == 0:
                        return result['result'][0]
                    else:
                        print(f"Baidu ASR error: {result['err_msg']}")
                        # 如果百度API失败，回退到原有的识别方法
                else:
                    # 使用原来的识别方法
                    # ... 原来的代码 ...
                    pass
            
            # 如果提供了音频文件路径
            elif audio_file_path is not None and os.path.exists(audio_file_path):
                if self.use_baidu and self.baidu_client:
                    with open(audio_file_path, 'rb') as f:
                        audio_data = f.read()
                    
                    result = self.baidu_client.asr(audio_data, 'wav', 16000, {
                        'dev_pid': 1537,  # 普通话(有标点)
                    })
                    
                    if result['err_no'] == 0:
                        return result['result'][0]
                    else:
                        print(f"Baidu ASR error: {result['err_msg']}")
                        # 如果百度API失败，回退到原有的识别方法
                else:
                    # 使用原来的识别方法
                    # ... 原来的代码 ...
                    pass
                    
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return None 