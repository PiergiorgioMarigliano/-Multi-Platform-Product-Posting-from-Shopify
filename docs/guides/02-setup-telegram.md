# Telegram Bot Setup Guide

This guide explains how to create a Telegram bot and configure it to automatically publish content to your channels.

**Estimated time**: 5-10 minutes
**Cost**: Free

## Table of Contents

1. [Create the Bot](#1-create-the-bot)
2. [Add the Bot as Channel Admin](#2-add-the-bot-as-channel-admin)
3. [Find the Channel IDs](#3-find-the-channel-ids)
4. [Verification Test](#4-verification-test)
5. [Configuration for Make.com](#5-configuration-for-makecom)
6. [Configuration for Python](#6-configuration-for-python)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Create the Bot

1. Open **Telegram** on your phone or desktop
2. Search for **`@BotFather`** (Telegram's official bot creation tool)
3. Start the chat and type: `/newbot`
4. BotFather will ask for a **display name** (e.g., `My Store Bot`)
5. Then it will ask for a **username** (must end with `bot`, e.g., `mystore_bot`)
6. BotFather will reply with the **token**:

```
Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

7. **Copy and save this token** in a secure place. You will need it for configuration.

> **WARNING**: Never share the token publicly. Anyone with the token can control the bot.

---

## 2. Add the Bot as Channel Admin

The bot must be a channel administrator in order to publish messages.

### For each channel:

1. Open the **Telegram channel** where you want to publish
2. Tap the **channel name** at the top to open channel info
3. Go to **"Administrators"**
4. Tap **"Add Administrator"**
5. Search for your bot (e.g., `@mystore_bot`)
6. Select it and configure permissions:
   - **"Post Messages"**: ✅ (REQUIRED)
   - Other permissions are optional
7. Confirm

**Repeat for the second channel.**

---

## 3. Find the Channel IDs

### Method 1: @userinfobot (Recommended)

1. Go to your Telegram channel
2. Take **any message** from the channel
3. **Forward it** to the bot `@userinfobot`
4. The bot will reply with the channel ID in the format: **`-100xxxxxxxxxx`**
5. Copy this ID

### Method 2: @getmyid_bot

1. Add `@getmyid_bot` to the channel as admin (temporarily)
2. Post something in the channel
3. The bot will reply with the ID
4. Remove the bot from admins if you no longer need it

### Method 3: Via Username (for public channels)

If your channel has a public username (e.g., `@mychannel`), you can use `@mychannel` directly instead of the numeric ID.

---

## 4. Verification Test

To verify everything works, open your browser and visit this URL (replace the placeholders):

```
https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text=Test%20Multi-Poster
```

Example:

```
https://api.telegram.org/bot123456789:ABCdefGHI/sendMessage?chat_id=-1001234567890&text=Test%20Multi-Poster
```

If you see the message "Test Multi-Poster" in the channel, **everything is working correctly!**

### Test with a Photo

```
https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHANNEL_ID}&photo=https://via.placeholder.com/400&caption=Test%20photo
```

---

## 5. Configuration for Make.com

If you're using Option A (Make.com):

1. In the Telegram Bot module on Make.com, click **"Create a connection"**
2. **Connection name**: `Multi-Poster Bot`
3. **Token**: paste the bot token
4. **Chat ID**: paste the channel ID (with the `-100` prefix)

---

## 6. Configuration for Python

If you're using Option B (Python script), add these values to the `.env` file:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL_ID_1=-1001234567890
TELEGRAM_CHANNEL_ID_2=-1009876543210
```

---

## 7. Troubleshooting

### "Bot is not a member of the channel chat"

The bot has not been added as a channel admin. Repeat [step 2](#2-add-the-bot-as-channel-admin).

### "Chat not found"

The channel ID is incorrect. Verify:
- The format must be `-100xxxxxxxxxx` (starts with `-100`)
- Use @userinfobot to double-check the ID

### "Not enough rights to send text messages"

The bot is in the channel but doesn't have publishing permission. Go to channel administrators and enable "Post Messages" for the bot.

### Photos aren't being sent

- Verify the file is in JPEG, PNG, or WebP format
- Photos must not exceed 10MB (20MB for documents)
- For videos: maximum 50MB, MP4 format

---

**Next step**: [Meta Developer Setup](03-setup-meta.md)
