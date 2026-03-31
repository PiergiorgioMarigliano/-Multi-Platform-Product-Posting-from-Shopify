# Make.com Setup Guide

This guide walks you through configuring the Make.com scenario that automates product distribution from Shopify to all your channels.

## Prerequisites

Before proceeding, make sure you have completed:

- [Telegram Bot Setup](02-setup-telegram.md)
- [Meta Developer Setup](03-setup-meta.md)
- An active Shopify store with at least one product

## Table of Contents

1. [Create a Make.com Account](#1-create-a-makecom-account)
2. [Create a New Scenario](#2-create-a-new-scenario)
3. [Configure the Shopify Trigger](#3-configure-the-shopify-trigger)
4. [Add the Router](#4-add-the-router)
5. [Configure Telegram (x2 channels)](#5-configure-telegram)
6. [Configure Facebook Pages](#6-configure-facebook-pages)
7. [Configure Instagram](#7-configure-instagram)
8. [Handle Carousels (Multiple Photos)](#8-handle-carousels)
9. [Test and Activate](#9-test-and-activate)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Create a Make.com Account

1. Go to [make.com](https://www.make.com) and sign up
2. The free plan includes 1,000 operations/month and 2 scenarios (enough for testing)
3. For production use, the **Core** plan (~9 EUR/month) provides 10,000 operations/month

> **Cost breakdown**: publishing 1 product to 4 channels uses approximately 6-8 operations. With the Core plan, you can publish over 1,000 products per month.

---

## 2. Create a New Scenario

1. From the dashboard, click **"Create a new scenario"**
2. The visual editor will open with an empty canvas

---

## 3. Configure the Shopify Trigger

1. Click the **"+"** circle in the center of the canvas
2. Search for **"Shopify"** in the module list
3. Select **"Watch Products"** (triggers when a product is created or updated)
4. Click **"Create a connection"**:
   - **Connection name**: `My Store`
   - **Store URL**: your Shopify URL (e.g., `my-store.myshopify.com`)
   - **API Key / Access Token**: you need a Shopify API token

### How to Get the Shopify API Token

1. Go to your Shopify admin panel: `https://my-store.myshopify.com/admin`
2. Navigate to **Settings** (bottom left) → **Apps and sales channels** → **Develop apps**
3. Click **"Create an app"** → give it a name (e.g., "Multi-Poster")
4. Go to **"Configure Admin API scopes"**
5. Select these permissions:
   - `read_products` (required)
   - `read_product_images` (required)
   - `read_product_listings` (recommended)
6. Click **"Save"** → **"Install app"**
7. Copy the **Admin API access token** (it is shown only once!)

Go back to Make.com and paste the token into the Shopify connection.

---

## 4. Add the Router

1. Click the arrow coming out of the Shopify module
2. Add a **"Router"** module (found under "Flow Control")
3. The Router creates parallel branches: each branch will send the product to a different channel

---

## 5. Configure Telegram

### Channel 1

1. From the Router, add a new branch
2. Search for **"Telegram Bot"** → select **"Send a Text Message or a Reply"** (for text + photo as a link) or **"Send a Photo"** (for photo with caption)
3. **Create a connection**: paste the bot token (from @BotFather)
4. **Chat ID**: paste the first channel ID (format: `-100xxxxxxxxxx`)
5. **Text/Caption**: map the Shopify fields. Example:

```
🛍️ {{1.title}}
💰 {{1.variants[].price}} EUR

{{1.body_html}}
```

> **Note**: `{{1.title}}` refers to the "Title" field from the Shopify module (#1). Click on the field and Make.com will show you the available data to map.

### Channel 2

1. Duplicate the Telegram module (right-click → "Clone module") or add a new branch from the Router
2. Change only the **Chat ID** to the second channel's ID
3. The rest of the configuration stays the same

---

## 6. Configure Facebook Pages

1. From the Router, add a new branch
2. Search for **"Facebook Pages"** → select **"Create a Post with Photos"**
3. **Create a connection**: Make.com will open the Facebook OAuth flow
   - Log in with your Facebook account
   - Authorize the Make.com app
   - Select your page when prompted
4. **Page**: select your page from the dropdown
5. **Photos URL**: map the Shopify image field: `{{1.images[].src}}`
6. **Message**: map title, price, and description as with Telegram

> **Advantage of Make.com**: Facebook token management (renewal, expiration) is completely automatic. You don't have to worry about anything.

---

## 7. Configure Instagram

1. From the Router, add a new branch
2. Search for **"Instagram for Business"** → select **"Create a Photo Post"**
3. **Create a connection**: use the same Facebook login (Make.com will automatically link the associated IG Professional account)
4. **Image URL**: map the Shopify image URL: `{{1.images[].src}}`

> **Important**: Instagram requires a publicly accessible URL for the image. Shopify image URLs (`cdn.shopify.com/...`) are public, so they work perfectly.

5. **Caption**: map the Shopify fields. You can add hashtags here:

```
🛍️ {{1.title}}
💰 {{1.variants[].price}} EUR

{{1.body_html}}

#shop #products #retail #offer
```

---

## 8. Handle Carousels

Shopify products can have multiple images. Here's how to handle carousels:

### Telegram (Media Group)

1. Replace the "Send a Photo" module with **"Send a Media Group"**
2. In the configuration, map the images array: `{{1.images[]}}`
3. Telegram supports up to 10 photos in a carousel

### Instagram (Carousel Post)

1. Use the **"Create a Carousel Post"** module instead of "Create a Photo Post"
2. Map the array of image URLs

### Facebook (Multi-Photo Post)

1. The "Create a Post with Photos" module already supports multiple photos
2. Map all images from the Shopify array

### Alternative Approach: Iterator

If you need more control:

1. After the Shopify trigger, add an **"Iterator"** module on the images array
2. The Iterator loops through each image
3. Connect each iteration to the desired channel
4. Use an **"Aggregator"** to reassemble the carousel where needed

---

## 9. Test and Activate

### Manual Test

1. Click **"Run once"** in the scenario canvas
2. Go to Shopify and create a test product (even with a placeholder image)
3. Go back to Make.com: you should see the modules activate in sequence
4. Verify that the product appeared on all channels
5. Delete the test product if needed

### Activation

1. If the test was successful, activate scheduling:
   - **"Immediately"**: the scenario triggers in real time via Shopify webhook
   - **Interval**: every 15 minutes (Core plan) or 5 minutes (Pro plan)
2. Click the **ON/OFF switch** at the bottom left to activate the scenario
3. The scenario is now live and will run automatically

### Monitoring

- Make.com displays the execution history in the **"History"** tab
- You can view each run, which modules were triggered, and any errors
- Configure email notifications for errors: **Scenario settings** → **Notifications**

---

## 10. Troubleshooting

### "Connection expired" on Facebook/Instagram

Make.com renews tokens automatically, but occasionally you may need to reauthorize:

1. Go to the Facebook/Instagram module connection settings
2. Click **"Reauthorize"**
3. Log in again with Facebook

### Images don't appear on Instagram

- Verify that the image URL is publicly accessible
- Shopify images must be in JPEG or PNG format
- The aspect ratio must be between 4:5 and 1.91:1

### The scenario doesn't trigger

- Verify that the ON/OFF switch is set to ON
- Check that the Shopify connection is active
- Try running "Run once" manually to diagnose

### "Rate limit" error on Telegram

- You should never reach the rate limit under normal use
- If it happens, add a **"Sleep"** module (1-2 seconds delay) between Telegram modules

---

**Next step**: [Telegram Bot Setup](02-setup-telegram.md)
