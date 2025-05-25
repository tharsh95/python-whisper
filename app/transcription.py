import whisper
import ssl
import certifi

def transcribe_audio(file_path: str) -> str:
    # Configure SSL context to use certifi's certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl._create_default_https_context = lambda: ssl_context
    
    # Initialize Whisper model
    model = whisper.load_model("base",device="cpu")
    
    # Transcribe the audio file
    result = model.transcribe(file_path,language="en")
    
    # Return the transcribed text
    return result["text"]