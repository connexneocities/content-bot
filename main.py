import os
import json
import numpy as np
from datetime import datetime

from news_fetcher import fetch_top_stories, get_best_story
from script_writer import write_script
from voice_gen import generate_voiceover
from video_maker import create_video
from poster import post_to_all_platforms

LOG_FILE = "output/run_log.json"


def log_run(story, script_data, success):
    """Log each run for tracking"""
    os.makedirs("output", exist_ok=True)

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append({
        "timestamp": str(datetime.now()),
        "story_title": story.get("title", ""),
        "category": story.get("category", ""),
        "video_title": script_data.get("title", ""),
        "posted": success
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs[-50:], f, indent=2)  # keep last 50 runs


def run_pipeline():
    print("=" * 60)
    print(f"🤖 CONTENT BOT STARTED — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # ── Step 1: Find trending news ────────────────────────────────
    print("\n📡 Step 1: Fetching news...")
    stories = fetch_top_stories(max_per_feed=3)
    if not stories:
        print("❌ No stories found. Exiting.")
        return

    story = get_best_story(stories)
    print(f"🔥 Selected: {story['title']}")

    # ── Step 2: Write scripts ─────────────────────────────────────
    print("\n✍️  Step 2: Writing script...")
    # Write for Instagram (YouTube version is the same script, slightly different CTA)
    script_data = write_script(story, platform="instagram")
    print(f"📝 Title: {script_data.get('title', '')}")

    # ── Step 3: Generate voiceover ────────────────────────────────
    print("\n🎙️  Step 3: Generating voiceover...")
    audio_path = generate_voiceover(
        script_data["script"],
        output_path="output/voiceover.mp3",
        speed="fast"
    )

    # ── Step 4: Create video ──────────────────────────────────────
    print("\n🎬 Step 4: Creating video...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    video_filename = f"video_{timestamp}.mp4"
    video_path = create_video(
        script_data,
        audio_path,
        category=story.get("category", "default"),
        output_filename=video_filename
    )

    # ── Step 5: Post to platforms ─────────────────────────────────
    print("\n🚀 Step 5: Posting to platforms...")
    results = post_to_all_platforms(video_path, script_data)

    # ── Log ───────────────────────────────────────────────────────
    success = any(results.values())
    log_run(story, script_data, success)

    print("\n" + "=" * 60)
    print(f"✅ PIPELINE COMPLETE — {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
