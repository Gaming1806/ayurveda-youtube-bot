#!/usr/bin/env python3
"""Fetch royalty‑free footage from Pexels (if key provided) or copy from local folder."""
import os, json, argparse, requests

PEXELS_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_AVAILABLE = bool(PEXELS_KEY)

def download(query: str, output_path: str = "footage.mp4"):
    if PEXELS_AVAILABLE:
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": PEXELS_KEY}
        params = {"query": query, "per_page": 1}
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        data = r.json()["videos"]
        if not data:
            raise SystemExit("❌ No footage found on Pexels.")
        video_url = data[0]["video_files"][0]["link"]  # highest quality ≤ 1080p
        with requests.get(video_url, stream=True) as vi:
            vi.raise_for_status()
            with open(output_path, "wb") as out:
                for chunk in vi.iter_content(chunk_size=8192):
                    out.write(chunk)
        print(f"✅ Footage downloaded from Pexels → {output_path} ({data[0]['duration']} s)")
        return
    # Fallback: copy a local file if it exists
    local = os.path.join(os.path.dirname(__file__), "..", "footage", query.replace(" ", "_") + ".mp4")
    if os.path.exists(local):
        import shutil
        shutil.copy(local, output_path)
        print(f"✅ Using local footage → {output_path}")
    else:
        raise SystemExit(f"❌ No local footage found at {local} and no Pexels key.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="Search query for footage")
    parser.add_argument("--output", default="footage.mp4", help="Output MP4 path")
    args = parser.parse_args()
    download(args.query, args.output)