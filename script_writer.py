import os
import requests
import json

# Using Google Gemini API - FREE tier (60 requests/min)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def write_script(story, platform="instagram"):
    """Generate an engaging script from a news story"""

    if platform == "instagram":
        duration = "45-60 seconds"
        style = "punchy, energetic, casual, use emojis in captions"
        format_note = "Hook (5 sec) → Context (15 sec) → Key Facts (20 sec) → Opinion/CTA (10 sec)"
    else:  # youtube shorts
        duration = "50-60 seconds"
        style = "informative but exciting, clear and simple language"
        format_note = "Hook (5 sec) → Story (30 sec) → Takeaway (15 sec) → Subscribe CTA (5 sec)"

    prompt = f"""
You are a viral social media content creator. Create a {duration} video script for {platform.upper()} about this news story.

NEWS TITLE: {story['title']}
NEWS SUMMARY: {story['summary'][:500]}
CATEGORY: {story['category']}

REQUIREMENTS:
- Style: {style}
- Format: {format_note}
- Start with a SHOCKING hook that stops the scroll
- Use simple language anyone can understand
- Make it feel urgent and exciting
- End with engagement CTA ("Follow for more", "Comment below", etc.)

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "catchy title for the video",
  "script": "full spoken script here",
  "caption": "social media caption with hashtags",
  "hashtags": ["tag1", "tag2", "tag3"],
  "hook": "just the opening line",
  "thumbnail_text": "bold text for thumbnail (max 6 words)"
}}
"""

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1000}
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, params=params, json=body)
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        # Clean and parse JSON
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)

    except Exception as e:
        print(f"Gemini error: {e}")
        # Fallback basic script
        return {
            "title": story["title"],
            "script": f"Breaking news! {story['title']}. {story['summary'][:200]}. Stay tuned for more updates!",
            "caption": f"{story['title']} #news #trending #viral",
            "hashtags": ["news", "trending", "viral", "breaking"],
            "hook": f"You won't believe what just happened!",
            "thumbnail_text": story["title"][:30]
        }


def write_scripts_for_both_platforms(story):
    """Generate scripts for Instagram and YouTube"""
    print("✍️ Writing Instagram script...")
    instagram_script = write_script(story, "instagram")

    print("✍️ Writing YouTube script...")
    youtube_script = write_script(story, "youtube")

    return {
        "instagram": instagram_script,
        "youtube": youtube_script
    }


if __name__ == "__main__":
    test_story = {
        "title": "Egypt Qualifies for World Cup Knockouts for First Time Ever",
        "summary": "Egypt made history at the 2026 FIFA World Cup by qualifying for the knockout rounds for the very first time in the nation's football history.",
        "category": "sports"
    }

    result = write_script(test_story, "instagram")
    print(json.dumps(result, indent=2))
