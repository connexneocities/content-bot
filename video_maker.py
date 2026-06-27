from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import requests
from io import BytesIO

OUTPUT_DIR = "output"
ASSETS_DIR = "assets"

# Video dimensions for Reels/Shorts (vertical)
WIDTH = 1080
HEIGHT = 1920

# Color themes per category
THEMES = {
    "sports":     {"bg": "#1a1a2e", "accent": "#e94560", "text": "#ffffff"},
    "world":      {"bg": "#0f3460", "accent": "#e94560", "text": "#ffffff"},
    "technology": {"bg": "#16213e", "accent": "#00b4d8", "text": "#ffffff"},
    "business":   {"bg": "#1b4332", "accent": "#40916c", "text": "#ffffff"},
    "default":    {"bg": "#1a1a2e", "accent": "#f72585", "text": "#ffffff"},
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_background_frame(title, hook, thumbnail_text, category="default", frame_num=0):
    """Create a single video frame as PIL Image"""
    theme = THEMES.get(category, THEMES["default"])
    bg_color = hex_to_rgb(theme["bg"])
    accent_color = hex_to_rgb(theme["accent"])
    text_color = hex_to_rgb(theme["text"])

    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    # Animated accent bar (moves slightly each frame)
    bar_y = 400 + (frame_num % 20)
    draw.rectangle([0, bar_y, WIDTH, bar_y + 8], fill=accent_color)

    # Category badge
    draw.rectangle([60, 160, 300, 220], fill=accent_color)
    try:
        font_badge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font_badge = ImageFont.load_default()
    draw.text((80, 172), category.upper(), fill=text_color, font=font_badge)

    # Main thumbnail text (big bold center text)
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font_big = font_med = font_small = ImageFont.load_default()

    # Thumbnail text
    wrapped = textwrap.wrap(thumbnail_text.upper(), width=14)
    y_pos = 500
    for line in wrapped[:3]:
        draw.text((WIDTH//2, y_pos), line, fill=text_color, font=font_big, anchor="mm")
        y_pos += 110

    # Hook text
    wrapped_hook = textwrap.wrap(hook, width=28)
    y_pos = max(y_pos + 80, 950)
    for line in wrapped_hook[:3]:
        draw.text((WIDTH//2, y_pos), line, fill=accent_color, font=font_med, anchor="mm")
        y_pos += 70

    # Bottom branding
    draw.rectangle([0, HEIGHT-120, WIDTH, HEIGHT], fill=accent_color)
    draw.text((WIDTH//2, HEIGHT-60), "FOLLOW FOR MORE 🔥", fill=text_color, font=font_med, anchor="mm")

    # Subtle animated dots
    for i in range(5):
        dot_x = 100 + i * 200 + (frame_num * 2 % 50)
        draw.ellipse([dot_x, HEIGHT-180, dot_x+20, HEIGHT-160], fill=accent_color)

    return img


def create_video(script_data, audio_path, category="default", output_filename="video.mp4"):
    """Create a full video from script data and audio"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, output_filename)

    title = script_data.get("title", "Breaking News")
    hook = script_data.get("hook", "You need to see this!")
    thumbnail_text = script_data.get("thumbnail_text", title[:30])

    print(f"🎬 Creating video: {title}")

    # Load audio
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    fps = 24
    total_frames = int(duration * fps)

    print(f"⏱️ Video duration: {duration:.1f}s | Frames: {total_frames}")

    # Generate frames
    frames = []
    for i in range(total_frames):
        frame = create_background_frame(title, hook, thumbnail_text, category, i)
        frames.append(np.array(frame))

    # Build video clip
    video_clip = ImageSequenceClip(frames, fps=fps)
    final = video_clip.set_audio(audio_clip)

    # Export
    print("💾 Exporting video...")
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=fps,
        verbose=False,
        logger=None
    )

    print(f"✅ Video saved: {output_path}")
    return output_path


if __name__ == "__main__":
    import numpy as np

    test_script = {
        "title": "Egypt Makes World Cup History",
        "hook": "You won't believe what just happened!",
        "thumbnail_text": "EGYPT MAKES HISTORY"
    }

    # Test frame generation
    frame = create_background_frame(
        test_script["title"],
        test_script["hook"],
        test_script["thumbnail_text"],
        "sports", 0
    )
    frame.save("output/test_frame.png")
    print("✅ Test frame saved to output/test_frame.png")
