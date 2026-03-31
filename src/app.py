"""
Multi-Poster: Streamlit interface for publishing products to all channels.
Upload photos + description → publishes to Telegram, WhatsApp, Facebook, Instagram.

Launch with: streamlit run app.py
"""
import streamlit as st
import os
import tempfile
from pathlib import Path

from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_IDS,
    WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_GROUP_IDS,
    META_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID, INSTAGRAM_ACCOUNT_ID,
)
from posters.telegram_poster import TelegramPoster
from posters.whatsapp_poster import WhatsAppPoster
from posters.meta_poster import MetaPoster


def check_config():
    """Check which services are properly configured."""
    services = {}
    services["telegram"] = bool(TELEGRAM_BOT_TOKEN and any(TELEGRAM_CHANNEL_IDS))
    services["whatsapp"] = bool(WHATSAPP_TOKEN and WHATSAPP_PHONE_NUMBER_ID and any(WHATSAPP_GROUP_IDS))
    services["facebook"] = bool(META_PAGE_ACCESS_TOKEN and FACEBOOK_PAGE_ID)
    services["instagram"] = bool(META_PAGE_ACCESS_TOKEN and INSTAGRAM_ACCOUNT_ID)
    return services


def save_uploaded_files(uploaded_files) -> list[str]:
    """Save uploaded files to a temporary directory and return their paths."""
    temp_dir = tempfile.mkdtemp()
    paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        paths.append(file_path)
    return paths


def main():
    st.set_page_config(
        page_title="Multi-Poster",
        page_icon="📦",
        layout="wide",
    )

    st.title("📦 Multi-Poster")
    st.markdown("**Upload once, publish everywhere.**")

    # --- Service status ---
    services = check_config()

    with st.sidebar:
        st.header("Service Status")
        for name, active in services.items():
            icon = "✅" if active else "❌"
            st.markdown(f"{icon} **{name.capitalize()}**")

        if not any(services.values()):
            st.error("No services configured! Please fill in .env")
            st.stop()

        st.divider()
        st.header("Channels to Publish")
        post_telegram = st.checkbox("Telegram", value=services["telegram"],
                                     disabled=not services["telegram"])
        post_whatsapp = st.checkbox("WhatsApp", value=services["whatsapp"],
                                     disabled=not services["whatsapp"])
        post_facebook = st.checkbox("Facebook", value=services["facebook"],
                                     disabled=not services["facebook"])
        post_instagram = st.checkbox("Instagram", value=services["instagram"],
                                      disabled=not services["instagram"])

    # --- Media upload ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Upload product photos/video")
        uploaded_files = st.file_uploader(
            "Drag and drop your images or video here",
            type=["jpg", "jpeg", "png", "webp", "mp4", "mov"],
            accept_multiple_files=True,
        )

        is_video = False
        if uploaded_files:
            # Show preview
            for f in uploaded_files:
                ext = Path(f.name).suffix.lower()
                if ext in (".mp4", ".mov"):
                    is_video = True
                    st.video(f)
                else:
                    st.image(f, width=200)

    with col2:
        st.subheader("2. Product description")
        product_name = st.text_input("Product name", placeholder="e.g., Nike Air Max 90 Shoes")
        price = st.text_input("Price", placeholder="e.g., 89.90 EUR")
        description = st.text_area(
            "Description",
            placeholder="Enter the product description...",
            height=150,
        )

        # Compose the final message
        caption_parts = []
        if product_name:
            caption_parts.append(f"🛍️ {product_name}")
        if price:
            caption_parts.append(f"💰 {price}")
        if description:
            caption_parts.append(f"\n{description}")

        caption = "\n".join(caption_parts)

        if caption:
            st.divider()
            st.markdown("**Message preview:**")
            st.text(caption)

    # --- Publishing ---
    st.divider()

    if st.button("🚀 PUBLISH TO ALL CHANNELS", type="primary",
                  use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one photo or video!")
            return
        if not caption.strip():
            st.error("Please enter at least a product name or description!")
            return

        # Save files temporarily
        media_paths = save_uploaded_files(uploaded_files)

        results = {}
        progress = st.progress(0)
        status = st.status("Publishing in progress...", expanded=True)

        total_steps = sum([post_telegram, post_whatsapp, post_facebook, post_instagram])
        current_step = 0

        # --- TELEGRAM ---
        if post_telegram:
            with status:
                st.write("📨 Sending to Telegram...")
            try:
                poster = TelegramPoster(TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_IDS)
                results["telegram"] = poster.publish(media_paths, caption, is_video)
            except Exception as e:
                results["telegram"] = {"error": str(e)}
            current_step += 1
            progress.progress(current_step / total_steps)

        # --- WHATSAPP ---
        if post_whatsapp:
            with status:
                st.write("📱 Sending to WhatsApp...")
            try:
                poster = WhatsAppPoster(WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID,
                                        WHATSAPP_GROUP_IDS)
                results["whatsapp"] = poster.publish(media_paths, caption, is_video)
            except Exception as e:
                results["whatsapp"] = {"error": str(e)}
            current_step += 1
            progress.progress(current_step / total_steps)

        # --- FACEBOOK ---
        if post_facebook:
            with status:
                st.write("📘 Publishing to Facebook...")
            try:
                poster = MetaPoster(META_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID,
                                    INSTAGRAM_ACCOUNT_ID)
                meta_results = poster.publish(media_paths, caption, is_video)
                results["facebook"] = meta_results.get("facebook", {})
                # Instagram is handled together with Facebook
                if post_instagram:
                    results["instagram"] = meta_results.get("instagram", {})
            except Exception as e:
                results["facebook"] = {"error": str(e)}
            current_step += 1
            progress.progress(current_step / total_steps)

        # --- INSTAGRAM (if not already handled with Facebook) ---
        if post_instagram and "instagram" not in results:
            with status:
                st.write("📸 Publishing to Instagram...")
            try:
                poster = MetaPoster(META_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID,
                                    INSTAGRAM_ACCOUNT_ID)
                meta_results = poster.publish(media_paths, caption, is_video)
                results["instagram"] = meta_results.get("instagram", {})
            except Exception as e:
                results["instagram"] = {"error": str(e)}
            current_step += 1
            progress.progress(current_step / total_steps)

        progress.progress(1.0)

        # --- SUMMARY ---
        with status:
            st.write("Done!")
        status.update(label="Publishing complete!", state="complete")

        st.subheader("Results")
        for service, result in results.items():
            if isinstance(result, dict) and result.get("error"):
                st.error(f"❌ **{service.capitalize()}**: {result['error']}")
            else:
                # Check if all sub-results are OK
                all_ok = True
                if isinstance(result, dict):
                    for k, v in result.items():
                        if isinstance(v, dict) and not v.get("success", True):
                            all_ok = False
                            st.warning(f"⚠️ **{service.capitalize()}** ({k}): {v.get('error', 'Error')}")
                if all_ok:
                    st.success(f"✅ **{service.capitalize()}**: Published successfully!")

        # Clean up temporary files
        for path in media_paths:
            try:
                os.remove(path)
            except OSError:
                pass


if __name__ == "__main__":
    main()
