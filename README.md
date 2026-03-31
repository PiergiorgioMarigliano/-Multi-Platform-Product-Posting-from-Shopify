# Multi-Poster

**Publish your products across all social and messaging channels with a single upload.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Shopify](https://img.shields.io/badge/Shopify-Integrated-96BF48?logo=shopify&logoColor=white)](https://shopify.com)
[![Make.com](https://img.shields.io/badge/Make.com-Automation-6D00CC?logo=make&logoColor=white)](https://make.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## The Problem

You run a retail shop and need to manually publish every new product on:

- 2 Telegram channels
- 2 WhatsApp groups
- Facebook Page
- Instagram Page
- Your website (Shopify)

Every new product means **6-7 manual operations** — uploading photos, copying descriptions, adjusting prices across platforms. **Time wasted: 15-20 minutes per product.**

## The Solution

**Multi-Poster** automates the entire workflow. You upload the product **once** on Shopify, and the system automatically distributes it to all configured channels.

```
                                    ┌──────────────────────┐
                                    │  Telegram Channel 1  │
                                    └──────────────────────┘
                                    ┌──────────────────────┐
                                    │  Telegram Channel 2  │
  ┌──────────┐    ┌──────────┐      └──────────────────────┘
  │ Shopify  │───▶│  Router  │─────▶┌──────────────────────┐
  │ (upload) │    │(Make.com)│      │  Facebook Page       │
  └──────────┘    └──────────┘      └──────────────────────┘
       │                            ┌──────────────────────┐
       │                            │  Instagram Business  │
       ▼                            └──────────────────────┘
  ┌──────────┐                      ┌──────────────────────┐
  │ Website  │                      │  WhatsApp (planned)  │
  │ (auto)   │                      └──────────────────────┘
  └──────────┘
```

**Time per product after setup: ~2 minutes** (just the Shopify upload).

---

## Architecture

The project offers **two operating modes**:

### Option A: Shopify + Make.com (Recommended)

| Feature | Detail |
|---|---|
| **Cost** | ~9 EUR/month (Make.com Core plan) |
| **Setup** | Visual, no-code |
| **Maintenance** | Near zero |
| **Website sync** | Automatic (Shopify handles it) |
| **Availability** | 24/7 (cloud-based) |

You upload the product to Shopify. A Make.com scenario detects the new product via webhook and distributes it to all channels in parallel.

### Option B: Standalone Python Script (Free)

| Feature | Detail |
|---|---|
| **Cost** | 0 EUR |
| **Setup** | Requires Python 3.10+ |
| **Maintenance** | Manual token renewal |
| **Website sync** | Separate process |
| **Availability** | Only when your PC is running |

A local Streamlit web app where you upload photos and a description, click a button, and the script publishes to all channels via API.

---

## Supported Channels

| Channel | Method | Media Support | Status |
|---|---|---|---|
| **Telegram** | Bot API | Single photo, carousel (up to 10), video | ✅ Active |
| **Facebook** | Graph API v21.0 | Single photo, carousel, video | ✅ Active |
| **Instagram** | Graph API v21.0 | Single photo, carousel, Reels | ✅ Active |
| **WhatsApp** | Cloud API (Groups) | Single photo, video | ⏸️ In development |

---

## Quick Start

### Option A: Shopify + Make.com

> Full guide: [`docs/guides/01-setup-make.md`](docs/guides/01-setup-make.md)

1. Set up the Telegram bot ([guide](docs/guides/02-setup-telegram.md))
2. Set up the Meta Developer app ([guide](docs/guides/03-setup-meta.md))
3. Create the scenario on Make.com ([guide](docs/guides/01-setup-make.md))
4. Connect Shopify as the trigger
5. Test with a sample product

### Option B: Python Script

> Full guide: [`docs/guides/04-setup-python.md`](docs/guides/04-setup-python.md)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/multi-poster.git
cd multi-poster

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
cp src/.env.example src/.env
# Edit src/.env with your tokens and IDs

# 5. Launch the app
cd src
streamlit run app.py
```

The interface will open in your browser at `http://localhost:8501`.

---

## Project Structure

```
multi-poster/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CHANGELOG.md                       # Change history
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Files excluded from Git
│
├── docs/
│   ├── guides/
│   │   ├── 01-setup-make.md           # Make.com setup guide
│   │   ├── 02-setup-telegram.md       # Telegram Bot setup guide
│   │   ├── 03-setup-meta.md           # Meta Developer setup guide
│   │   └── 04-setup-python.md         # Python script setup guide
│   └── images/
│       └── make-scenario.png          # Make.com scenario screenshot
│
├── src/
│   ├── app.py                         # Streamlit interface
│   ├── config.py                      # Configuration manager
│   ├── .env.example                   # Environment variables template
│   └── posters/
│       ├── __init__.py
│       ├── telegram_poster.py         # Telegram Bot API module
│       ├── whatsapp_poster.py         # WhatsApp Cloud API module
│       └── meta_poster.py            # Facebook + Instagram module
│
└── .github/
    ├── ISSUE_TEMPLATE.md              # Issue template
    └── CONTRIBUTING.md                # Contribution guidelines
```

---

## Screenshots

### Make.com Scenario

The Make.com scenario distributes products from Shopify to all channels in parallel:

![Make.com Scenario](docs/images/make-scenario.png)

### Python Interface (Streamlit)

The local interface allows manual publishing with a single click:

```
+--------------------------------------------------+
|  Multi-Poster                                     |
|                                                   |
|  [Upload photos/video]     Product name: ___      |
|  [photo1.jpg] [photo2.jpg] Price: ___             |
|                             Description: ___      |
|                                                   |
|  [  PUBLISH TO ALL CHANNELS  ]                    |
|                                                   |
|  Results:                                         |
|  ✅ Telegram (channel 1)                          |
|  ✅ Telegram (channel 2)                          |
|  ✅ Facebook                                      |
|  ✅ Instagram                                     |
+--------------------------------------------------+
```

---

## Configuration

### Environment Variables

The project uses a `.env` file for credentials. Copy `.env.example` and fill in your values:

| Variable | Description | Where to find it |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | @BotFather on Telegram |
| `TELEGRAM_CHANNEL_ID_1` | First channel ID | @userinfobot on Telegram |
| `TELEGRAM_CHANNEL_ID_2` | Second channel ID | @userinfobot on Telegram |
| `META_PAGE_ACCESS_TOKEN` | Facebook page token | Graph API Explorer |
| `FACEBOOK_PAGE_ID` | Facebook page ID | Graph API Explorer → `me/accounts` |
| `INSTAGRAM_ACCOUNT_ID` | IG Professional account ID | Graph API Explorer → `/{page-id}?fields=instagram_business_account` |
| `WHATSAPP_TOKEN` | WhatsApp Cloud API token | Meta Developer Dashboard |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp phone number ID | Meta Developer Dashboard |
| `WHATSAPP_GROUP_ID_1` | First WhatsApp group ID | WhatsApp Cloud API |
| `WHATSAPP_GROUP_ID_2` | Second WhatsApp group ID | WhatsApp Cloud API |

---

## Technical Limits

| Platform | Limit | Notes |
|---|---|---|
| **Telegram** | 30 msg/sec, carousel max 10 photos, video max 50MB | No practical limits for normal use |
| **Facebook** | 50 posts/day | More than sufficient for retail |
| **Instagram** | 50 posts/24h, photo ratio 4:5 to 1.91:1, width 320-1440px | Reels: 3-90 seconds |
| **WhatsApp** | 1,000 free conversations/month | Groups API currently in beta |
| **Make.com Core** | 10,000 operations/month, 1GB data transfer | Supports ~100-150 products/month with images |

---

## Roadmap

- [x] Telegram integration (Bot API)
- [x] Facebook integration (Graph API)
- [x] Instagram integration (Graph API)
- [x] Make.com scenario with Shopify trigger
- [x] Standalone Streamlit interface
- [ ] WhatsApp Groups integration
- [ ] Advanced carousel support on Make.com (multi-photo from Shopify)
- [ ] Error notifications via email
- [ ] Dashboard with publication history
- [ ] Scheduled posting (publish at specific times)

---

## Tech Stack

- **[Python 3.10+](https://python.org)** — Primary language
- **[Streamlit](https://streamlit.io)** — Local web interface
- **[Make.com](https://make.com)** — No-code automation platform
- **[Shopify API](https://shopify.dev)** — New product trigger
- **[Telegram Bot API](https://core.telegram.org/bots/api)** — Channel publishing
- **[Meta Graph API v21.0](https://developers.facebook.com/docs/graph-api/)** — Facebook + Instagram publishing

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Piergiorgio Marigliano**

Researcher in Statistics & Quantitative Methods | Python Developer

---

<p align="center">
  <i>Born from the real-world need to automate multichannel product management for a retail shop.</i>
</p>
