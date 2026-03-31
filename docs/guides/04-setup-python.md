# Python Script Setup Guide (Option B)

This guide explains how to install and configure the standalone Python script with Streamlit interface for manual product publishing.

**Estimated time**: 15-30 minutes
**Cost**: Free
**Requirements**: Python 3.10+

## Table of Contents

1. [System Requirements](#1-system-requirements)
2. [Installation](#2-installation)
3. [Credential Configuration](#3-credential-configuration)
4. [Launch the Application](#4-launch-the-application)
5. [Daily Usage](#5-daily-usage)
6. [Code Structure](#6-code-structure)
7. [Customization](#7-customization)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. System Requirements

- **Python 3.10+**: [Download](https://www.python.org/downloads/)
- **pip**: included with Python
- **Operating system**: Windows, macOS, or Linux
- **Internet connection**: required for API calls

### Verify Python Installation

```bash
python --version
# Expected output: Python 3.10.x or higher

pip --version
# Expected output: pip 2x.x.x
```

> **Windows**: if `python` is not recognized, try `python3` or verify that Python is in your system PATH.

---

## 2. Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/multi-poster.git
cd multi-poster

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

The project uses only three external libraries:

| Library | Version | Purpose |
|---|---|---|
| `streamlit` | >= 1.30.0 | Web interface |
| `requests` | >= 2.31.0 | HTTP calls to APIs |
| `python-dotenv` | >= 1.0.0 | Environment variable loading |

---

## 3. Credential Configuration

### Create the .env File

```bash
cd src
cp .env.example .env
```

Open `.env` with a text editor and fill in all the fields:

```env
# TELEGRAM
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL_ID_1=-1001234567890
TELEGRAM_CHANNEL_ID_2=-1009876543210

# META (Facebook + Instagram)
META_PAGE_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxx
FACEBOOK_PAGE_ID=1403696172988698
INSTAGRAM_ACCOUNT_ID=17841400xxxxxxxx

# WHATSAPP (optional - in development)
WHATSAPP_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_GROUP_ID_1=
WHATSAPP_GROUP_ID_2=
```

### Where to Find the Values

| Value | Guide |
|---|---|
| Telegram Token | [Telegram Setup](02-setup-telegram.md) → Step 1 |
| Telegram Channel IDs | [Telegram Setup](02-setup-telegram.md) → Step 3 |
| Meta Token / Page ID | [Meta Setup](03-setup-meta.md) → Steps 4-6 |
| Instagram ID | [Meta Setup](03-setup-meta.md) → Step 5 |
| WhatsApp credentials | [Meta Setup](03-setup-meta.md) → Step 9 |

> **SECURITY**: the `.env` file contains your credentials. Never upload it to GitHub (it's already included in `.gitignore`).

---

## 4. Launch the Application

```bash
cd src
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`.

### First Run

On the first launch, the sidebar will display the status of configured services:

- ✅ Service configured and ready
- ❌ Service not configured (missing credentials in `.env`)

---

## 5. Daily Usage

### Publishing a Product

1. **Launch the app** with `streamlit run app.py` (if not already running)
2. In the sidebar, **select the channels** you want to publish to
3. **Upload photos** (or video) by dragging them into the upload area
4. **Fill in the fields**: product name, price, description
5. Click **"PUBLISH TO ALL CHANNELS"**
6. Wait for completion and verify the results

### Supported Content Types

| Type | Formats | Notes |
|---|---|---|
| **Single photo** | JPG, JPEG, PNG, WebP | Max 10MB for Telegram |
| **Carousel** | Multiple photos uploaded together | Max 10 photos for Telegram |
| **Video** | MP4, MOV | Max 50MB for Telegram |

### Tips

- You can publish to specific channels only by unchecking the others in the sidebar
- The message preview updates in real time as you type
- You can upload multiple photos at once to create a carousel

---

## 6. Code Structure

```
src/
├── app.py                  # Main Streamlit interface
├── config.py               # Configuration loader from .env
├── .env                    # Your credentials (NOT tracked by Git)
├── .env.example            # Credentials template
└── posters/
    ├── __init__.py
    ├── telegram_poster.py  # Telegram Bot API
    ├── whatsapp_poster.py  # WhatsApp Cloud API
    └── meta_poster.py      # Facebook Graph API + Instagram
```

### Module Architecture

Each module in `posters/` follows the same structure:

1. **`__init__`**: initializes the connection with token and IDs
2. **`post_single_photo()`**: publishes a single photo with caption
3. **`post_video()`**: publishes a video
4. **`post_media_group()` / `post_carousel()`**: publishes multiple photos
5. **`publish()`**: unified method that automatically selects the correct type

---

## 7. Customization

### Modify the Message Template

In `app.py`, find the section where the `caption` is composed:

```python
caption_parts = []
if product_name:
    caption_parts.append(f"🛍️ {product_name}")
if price:
    caption_parts.append(f"💰 {price}")
if description:
    caption_parts.append(f"\n{description}")
```

You can customize it however you want, for example by adding hashtags or links:

```python
caption_parts.append("\n\n#shop #products #retail #offer")
caption_parts.append("🔗 www.yourwebsite.com")
```

### Add New Channels

To add a new channel (e.g., Twitter/X):

1. Create a new file `posters/twitter_poster.py`
2. Implement the class with standard methods (`publish()`, `post_single_photo()`, etc.)
3. Import it in `app.py` and add a checkbox in the sidebar
4. Add the publishing section in the main flow

---

## 8. Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

If you're using a virtual environment, make sure it's activated.

### "Connection refused" on localhost:8501

Streamlit might be running on a different port. Check the terminal for the correct URL.

### API Timeout Error

APIs have a 60-120 second timeout. If the video is very large, you may need to increase it:

```python
# In the poster module, increase the timeout
resp = requests.post(url, ..., timeout=300)  # 5 minutes
```

### Meta Token Expired

Tokens from the Graph API Explorer expire after 1-2 hours. For the Python script, it's essential to generate a long-lived token. See the [Meta guide](03-setup-meta.md#6-long-lived-token).

### Uploaded Photos Are Too Large

Streamlit has a default upload limit of 200MB. For the APIs:
- Telegram: max 10MB for photos, 50MB for videos
- Instagram: max 8MB for photos
- Facebook: max 10MB for photos, 1GB for videos

---

**Next step**: Go back to the [README](../../README.md) for the full overview.
