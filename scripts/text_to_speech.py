#!/usr/bin/env python3
"""Text‑to‑Speech using ElevenLabs (if key provided) or offline pyttsx3."""
import os, argparse
try:
    from elevenlabs import generate, save as elevenlabs_save
    ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_AVAILABLE = bool(ELEVENLABS_KEY)
except Exception:
    ELEVENLABS_AVAILABLE = False

def tts(text: str, output_path: str = "voiceover.mp3", voice: str = "Emma"):
    if ELEVENLABS_AVAILABLE:
        audio = generate(text=text, voice=voice, model="eleven_monolingual_v1")
        elevenlabs_save(audio, output_path)
        print(f"✅ TTS saved to {output_path} (ElevenLabs)")
        return
    # Fallback to offline pyttsx3
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    print(f"✅ TTS saved to {output_path} (offline pyttsx3)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Script text")
    parser.add_argument("--output", default="voiceover.mp3", help="Output MP3 path")
    parser.add_argument("--voice", default="Emma", help="ElevenLabs voice name")
    args = parser.parse_args()
    tts(args.text, args.output, args.voice)