from gtts import gTTS
from pydub import AudioSegment
import os

def generate_voiceover(script_text, output_path="output/voiceover.mp3", lang="en", speed="normal"):
    """
    Convert script to voice using gTTS - completely FREE
    No API key needed!
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Clean script - remove stage directions in brackets
    import re
    clean_text = re.sub(r'\[.*?\]', '', script_text)
    clean_text = re.sub(r'\(.*?\)', '', clean_text)
    clean_text = clean_text.strip()

    print(f"🎙️ Generating voiceover ({len(clean_text)} chars)...")

    # gTTS - Google Text to Speech (FREE)
    tts = gTTS(text=clean_text, lang=lang, slow=False)
    tts.save(output_path)

    # Speed up audio slightly for more energy (optional)
    if speed == "fast":
        audio = AudioSegment.from_mp3(output_path)
        faster = audio.speedup(playback_speed=1.15)
        faster.export(output_path, format="mp3")

    print(f"✅ Voiceover saved: {output_path}")
    return output_path


def get_audio_duration(audio_path):
    """Get duration of audio file in seconds"""
    audio = AudioSegment.from_mp3(audio_path)
    return len(audio) / 1000.0


if __name__ == "__main__":
    test_script = """
    Breaking news! Egypt just made history at the 2026 World Cup!
    For the first time EVER, Egypt has qualified for the knockout rounds.
    After a dramatic 1-1 draw with Iran, Egypt secured their historic spot.
    The entire nation is celebrating right now.
    Follow for more World Cup updates!
    """

    path = generate_voiceover(test_script, "output/test_voice.mp3", speed="fast")
    duration = get_audio_duration(path)
    print(f"⏱️ Duration: {duration:.1f} seconds")
