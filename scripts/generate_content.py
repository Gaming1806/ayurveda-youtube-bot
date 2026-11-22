#!/usr/bin/env python3
"""Generate Ayurvedic video content using OpenAI (or fallback to a static example)."""
import os, json, sys
try:
    import openai
    KEY = os.getenv("OPENAI_API_KEY")
    if KEY:
        openai.api_key = KEY
except Exception:
    openai = None

def generate(topic: str = "Ayurvedic home remedy for acidity") -> dict:
    # If OpenAI key is present, call the model; otherwise return a hard‑canned example.
    if openai:
        prompt = f"""
You are a certified Ayurveda health coach. Create the following for a YouTube video about "{topic}":
1) A 300‑word script (hook, body, CTA).
2) A 50‑character title (include the primary keyword).
3) A 2‑sentence description (include a disclaimer: "Not medical advice").
5) 8 tags (mix of broad & long‑tail).
Return **pure JSON** with keys: "script","title","description","tags".
"""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n",1)[1].rsplit("```",1)[0].strip()
        data = json.loads(raw)
        return data
    else:
        # Static fallback – replace with a local LLM call if desired.
        return {
            "script": "Did you know acidity can be soothed with a simple ginger‑lemon tea? Try this natural remedy today!",
            "title": "Instant Acid Relief – Ayurvedic Home Remedy",
            "description": "Learn how to balance Pitta dosha with this quick ginger‑lemon tea. Not medical advice.",
            "tags": ["ayurveda", "acidity", "ginger lemon tea", "pitta balance", "home remedy", "wellness", "natural cure", "ayurvedic tips"]
        }

if __name__ == "__main__":
    topic = os.getenv("TOPIC", "Ayurvedic home remedy for acidity")
    result = generate(topic)
    print(json.dumps(result, ensure_ascii=False, indent=2))