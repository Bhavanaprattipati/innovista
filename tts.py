from TTS.api import TTS
import os
from io import BytesIO

# Load model once
tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

def generate_audio(text, speaker="thorsten", language="en"):
    file_path = "output.wav"

    try:
        # Remove existing file if any
        if os.path.exists(file_path):
            os.remove(file_path)

        # Primary TTS generation using Coqui
        tts_model.tts_to_file(text=text, speaker=speaker, language=language, file_path=file_path)

        with open(file_path, "rb") as f:
            audio_bytes = BytesIO(f.read())

        return audio_bytes

    except Exception as e:
        print(f"⚠️ Coqui TTS failed: {e}")
        print("🔁 Falling back to IBM Granite TTS...")

        # --- PLACEHOLDER for IBM Granite TTS Integration ---
        try:
            # Simulated IBM Granite fallback (replace with actual API call if available)
            # Example: granite_audio_bytes = ibm_granite_generate_audio(text, language)

            fake_audio = BytesIO()
            fake_audio.write(b"IBM Granite fallback audio")  # Dummy placeholder
            fake_audio.seek(0)
            return fake_audio

        except Exception as ibm_e:
            print(f"❌ IBM Granite TTS also failed: {ibm_e}")
            raise RuntimeError("All TTS methods failed.")

def get_speakers_and_languages():
    return tts_model.speakers, tts_model.languages
