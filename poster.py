import os
import requests
import json
import time

# ── credentials from GitHub Secrets ──────────────────────────────────────────
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_USER_ID      = os.environ.get("INSTAGRAM_USER_ID", "")
YOUTUBE_API_KEY        = os.environ.get("YOUTUBE_API_KEY", "")

# For YouTube uploads we use OAuth – token stored as secret
YOUTUBE_REFRESH_TOKEN  = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")
YOUTUBE_CLIENT_ID      = os.environ.get("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET  = os.environ.get("YOUTUBE_CLIENT_SECRET", "")

# ── Video hosting (needed so Instagram can pull the file via URL) ─────────────
# Free option: upload to Cloudinary free tier, then pass the URL to Instagram
CLOUDINARY_CLOUD_NAME  = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY     = os.environ.get("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET  = os.environ.get("CLOUDINARY_API_SECRET", "")


# ─────────────────────────────────────────────────────────────────────────────
# CLOUDINARY – free video hosting (needed for Instagram API)
# ─────────────────────────────────────────────────────────────────────────────
def upload_to_cloudinary(video_path):
    """Upload video to Cloudinary free tier and return public URL"""
    import cloudinary
    import cloudinary.uploader

    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )

    print("☁️  Uploading video to Cloudinary...")
    result = cloudinary.uploader.upload(
        video_path,
        resource_type="video",
        folder="content-bot"
    )
    url = result["secure_url"]
    print(f"✅ Uploaded: {url}")
    return url


# ─────────────────────────────────────────────────────────────────────────────
# INSTAGRAM – Reels via Graph API
# ─────────────────────────────────────────────────────────────────────────────
def post_to_instagram(video_url, caption):
    """Post a Reel to Instagram using the Graph API"""
    if not INSTAGRAM_ACCESS_TOKEN or not INSTAGRAM_USER_ID:
        print("⚠️  Instagram credentials missing – skipping")
        return False

    base = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}"

    # Step 1 – create media container
    print("📸 Creating Instagram media container...")
    r = requests.post(f"{base}/media", params={
        "media_type":   "REELS",
        "video_url":    video_url,
        "caption":      caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    })
    data = r.json()
    if "id" not in data:
        print(f"❌ Container error: {data}")
        return False

    container_id = data["id"]
    print(f"   Container ID: {container_id}")

    # Step 2 – wait for processing (up to 2 min)
    print("⏳ Waiting for Instagram to process video...")
    for _ in range(12):
        time.sleep(10)
        status_r = requests.get(f"https://graph.facebook.com/v19.0/{container_id}", params={
            "fields":       "status_code",
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        })
        status = status_r.json().get("status_code", "")
        print(f"   Status: {status}")
        if status == "FINISHED":
            break
        if status == "ERROR":
            print("❌ Processing failed")
            return False

    # Step 3 – publish
    print("🚀 Publishing to Instagram...")
    pub_r = requests.post(f"{base}/media_publish", params={
        "creation_id":  container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    })
    pub_data = pub_r.json()
    if "id" in pub_data:
        print(f"✅ Instagram Reel posted! ID: {pub_data['id']}")
        return True

    print(f"❌ Publish error: {pub_data}")
    return False


# ─────────────────────────────────────────────────────────────────────────────
# YOUTUBE – Shorts upload via Data API v3
# ─────────────────────────────────────────────────────────────────────────────
def get_youtube_access_token():
    """Exchange refresh token for a short-lived access token"""
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id":     YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "refresh_token": YOUTUBE_REFRESH_TOKEN,
        "grant_type":    "refresh_token",
    })
    return r.json().get("access_token")


def post_to_youtube(video_path, title, description, tags):
    """Upload a Short to YouTube"""
    if not YOUTUBE_REFRESH_TOKEN:
        print("⚠️  YouTube credentials missing – skipping")
        return False

    access_token = get_youtube_access_token()
    if not access_token:
        print("❌ Could not get YouTube access token")
        return False

    print("▶️  Uploading to YouTube Shorts...")

    # Add #Shorts to description so YouTube treats it as a Short
    full_description = f"{description}\n\n#Shorts #News #Trending"

    metadata = {
        "snippet": {
            "title":       title[:100],           # YT limit
            "description": full_description[:5000],
            "tags":        tags[:500],
            "categoryId":  "25",                  # News & Politics
        },
        "status": {"privacyStatus": "public"},
    }

    # Resumable upload
    init_r = requests.post(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        headers={
            "Authorization":  f"Bearer {access_token}",
            "Content-Type":   "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
        },
        data=json.dumps(metadata)
    )

    upload_url = init_r.headers.get("Location")
    if not upload_url:
        print(f"❌ Could not get upload URL: {init_r.text}")
        return False

    with open(video_path, "rb") as f:
        video_data = f.read()

    upload_r = requests.put(
        upload_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type":  "video/mp4",
        },
        data=video_data
    )

    if upload_r.status_code in (200, 201):
        video_id = upload_r.json().get("id")
        print(f"✅ YouTube Short posted! https://youtube.com/shorts/{video_id}")
        return True

    print(f"❌ YouTube upload error: {upload_r.status_code} {upload_r.text}")
    return False


# ─────────────────────────────────────────────────────────────────────────────
# MASTER poster
# ─────────────────────────────────────────────────────────────────────────────
def post_to_all_platforms(video_path, script_data):
    results = {}

    caption   = script_data.get("caption", "")
    title     = script_data.get("title", "Breaking News")
    hashtags  = script_data.get("hashtags", [])

    # Instagram needs a public URL
    if CLOUDINARY_CLOUD_NAME:
        video_url = upload_to_cloudinary(video_path)
        results["instagram"] = post_to_instagram(video_url, caption)
    else:
        print("⚠️  Cloudinary not configured – skipping Instagram")
        results["instagram"] = False

    # YouTube takes the local file
    results["youtube"] = post_to_youtube(video_path, title, caption, hashtags)

    print("\n📊 Posting Summary:")
    for platform, success in results.items():
        icon = "✅" if success else "❌"
        print(f"   {icon} {platform.capitalize()}")

    return results


if __name__ == "__main__":
    print("Poster module loaded. Run main.py to execute the full pipeline.")
