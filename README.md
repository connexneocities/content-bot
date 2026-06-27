# 🤖 AI Content Bot — Free Automated Content Machine

Posts AI-generated videos to Instagram Reels & YouTube Shorts every 6 hours.
**Total cost: ₹0**

---

## 🏗️ Architecture

```
GitHub Actions (runs free every 6 hrs)
    ↓
news_fetcher.py   → grabs trending stories from RSS feeds
script_writer.py  → Gemini AI writes the script
voice_gen.py      → gTTS converts script to speech
video_maker.py    → MoviePy builds the video
poster.py         → posts to Instagram + YouTube
```

---

## 🚀 Setup Guide (Step by Step)

### Step 1 — Fork this repo on GitHub
- Go to github.com → New Repository → name it `content-bot`
- Upload all these files

### Step 2 — Get your FREE API keys

#### 🔵 Gemini API (script writing — FREE)
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

#### 📸 Instagram (posting Reels)
1. Create a Facebook Developer account: https://developers.facebook.com
2. Create an App → Add Instagram Graph API
3. Get your `Access Token` and `Instagram User ID`
4. Full guide: https://developers.facebook.com/docs/instagram-api

#### ▶️ YouTube (posting Shorts)
1. Go to: https://console.cloud.google.com
2. Create project → Enable "YouTube Data API v3"
3. Create OAuth credentials
4. Get refresh token using: https://developers.google.com/oauthplayground
5. Full guide: https://developers.google.com/youtube/v3/guides/uploading_a_video

#### ☁️ Cloudinary (free video hosting — needed for Instagram)
1. Sign up free at: https://cloudinary.com
2. Go to Dashboard → copy Cloud Name, API Key, API Secret

---

### Step 3 — Add secrets to GitHub

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these one by one:

| Secret Name | Where to get it |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio |
| `INSTAGRAM_ACCESS_TOKEN` | Facebook Developer Portal |
| `INSTAGRAM_USER_ID` | Facebook Developer Portal |
| `YOUTUBE_CLIENT_ID` | Google Cloud Console |
| `YOUTUBE_CLIENT_SECRET` | Google Cloud Console |
| `YOUTUBE_REFRESH_TOKEN` | OAuth Playground |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary Dashboard |
| `CLOUDINARY_API_KEY` | Cloudinary Dashboard |
| `CLOUDINARY_API_SECRET` | Cloudinary Dashboard |

---

### Step 4 — Test it manually
1. Go to your repo → **Actions** tab
2. Click **"Content Bot - Auto Post"**
3. Click **"Run workflow"**
4. Watch it run! ✅

---

### Step 5 — Let it run automatically
The bot runs automatically at:
- 6:00 AM UTC
- 12:00 PM UTC
- 6:00 PM UTC
- 12:00 AM UTC

That's **4 posts per day** on autopilot. 🎉

---

## 📁 File Structure

```
content-bot/
├── main.py            ← master controller
├── news_fetcher.py    ← gets trending news (RSS, free)
├── script_writer.py   ← AI writes scripts (Gemini, free)
├── voice_gen.py       ← text to speech (gTTS, free)
├── video_maker.py     ← builds the video (MoviePy, free)
├── poster.py          ← posts to Instagram + YouTube
├── requirements.txt   ← Python dependencies
├── assets/            ← put background images here (optional)
├── output/            ← generated videos saved here
└── .github/
    └── workflows/
        └── run_bot.yml ← GitHub Actions schedule
```

---

## 💰 Monetization Timeline

| Milestone | Action |
|---|---|
| 500 followers | Apply for brand collaborations |
| 1,000 YouTube subs | Enable YouTube monetization |
| 5,000 Instagram followers | Charge ₹5,000–15,000/sponsored post |
| 10,000 followers | ₹20,000–50,000/month easily |

---

## 🛠️ Customization

**Change niche** → Edit `RSS_FEEDS` in `news_fetcher.py`

**Change posting time** → Edit cron in `.github/workflows/run_bot.yml`

**Change video style** → Edit `THEMES` in `video_maker.py`

**Post more often** → Add more cron times (GitHub gives 2,000 free minutes/month)

---

## ❓ Troubleshooting

**Bot runs but doesn't post?**
→ Check GitHub Actions logs → Secrets tab → make sure all keys are added

**Video looks bad?**
→ Add background images to `/assets/` folder

**Instagram keeps failing?**
→ Make sure your Instagram account is a **Professional/Creator** account

---

Built with ❤️ using Python, Gemini AI, gTTS, MoviePy, and GitHub Actions.
