#!/usr/bin/env python3
"""Combine voiceover MP3 with footage MP4 using FFmpeg.
Produces a final MP4 (1280×720) with the audio muxed in."""
import subprocess, argparse, os

def merge(voice: str, footage: str, output: str = "final_video.mp4", duration: int = 60):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

    # FFmpeg command: scale footage if needed, mux audio
    cmd = [
        "ffmpeg", "-y",
        "-i", footage,
        "-i", voice,
        "-filter_complex",
        f"[0:v]scale=1280:720[vid];[1:a]atrim=duration={duration}[aud]",
        "-map", "[vid]",
        "-map", "[aud]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Video assembled → {output} ({duration}s)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", required=True, help="Path to voiceover MP3")
    parser.add_argument("--footage", required=True, help="Path to footage MP4")
    parser.add_argument("--output", default="final_video.mp4", help="Output MP4 path")
    parser.add_argument("--duration", type=int, default=60, help="Target video duration (seconds)")
    args = parser.parse_args()
    merge(args.voice, args.footage, args.output, args.duration)