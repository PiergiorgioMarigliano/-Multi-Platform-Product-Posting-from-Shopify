"""
Module for publishing to Telegram channels via Bot API.
Supports: single photo, carousel (media group), video.
"""
import requests
import os
import json
from typing import Optional


class TelegramPoster:
    """Handles publishing content to Telegram channels via the Bot API."""

    BASE_URL = "https://api.telegram.org/bot{token}"

    def __init__(self, bot_token: str, channel_ids: list[str]):
        """
        Initialize the Telegram poster.

        Args:
            bot_token: Bot token obtained from @BotFather.
            channel_ids: List of channel IDs (format: -100xxxxxxxxxx).
        """
        self.bot_token = bot_token
        self.channel_ids = channel_ids
        self.base_url = self.BASE_URL.format(token=bot_token)

    def _send_request(self, method: str, data: dict, files: dict = None) -> dict:
        """Send a request to the Telegram Bot API."""
        url = f"{self.base_url}/{method}"
        resp = requests.post(url, data=data, files=files, timeout=120)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("ok"):
            raise Exception(f"Telegram API error: {result.get('description', 'Unknown error')}")
        return result

    def post_single_photo(self, channel_id: str, photo_path: str, caption: str) -> dict:
        """Send a single photo with caption."""
        with open(photo_path, "rb") as photo:
            return self._send_request(
                "sendPhoto",
                data={"chat_id": channel_id, "caption": caption, "parse_mode": "HTML"},
                files={"photo": photo},
            )

    def post_video(self, channel_id: str, video_path: str, caption: str,
                   thumbnail_path: Optional[str] = None) -> dict:
        """Send a video with caption."""
        files = {"video": open(video_path, "rb")}
        if thumbnail_path:
            files["thumbnail"] = open(thumbnail_path, "rb")
        try:
            return self._send_request(
                "sendVideo",
                data={"chat_id": channel_id, "caption": caption, "parse_mode": "HTML"},
                files=files,
            )
        finally:
            for f in files.values():
                f.close()

    def post_media_group(self, channel_id: str, media_paths: list[str],
                         caption: str) -> dict:
        """
        Send a carousel of photos (media group).
        The caption is attached only to the first photo.
        """
        media_list = []
        files = {}

        for i, path in enumerate(media_paths):
            attach_name = f"photo_{i}"
            ext = os.path.splitext(path)[1].lower()

            if ext in (".mp4", ".mov", ".avi"):
                media_type = "video"
            else:
                media_type = "photo"

            media_item = {
                "type": media_type,
                "media": f"attach://{attach_name}",
            }
            if i == 0:
                media_item["caption"] = caption
                media_item["parse_mode"] = "HTML"

            media_list.append(media_item)
            files[attach_name] = open(path, "rb")

        try:
            return self._send_request(
                "sendMediaGroup",
                data={
                    "chat_id": channel_id,
                    "media": json.dumps(media_list),
                },
                files=files,
            )
        finally:
            for f in files.values():
                f.close()

    def publish(self, media_paths: list[str], caption: str,
                is_video: bool = False) -> dict:
        """
        Publish to all configured channels.
        Automatically selects: single photo, video, or carousel.

        Returns:
            Dictionary mapping channel IDs to their results.
        """
        results = {}
        for channel_id in self.channel_ids:
            try:
                if is_video:
                    result = self.post_video(channel_id, media_paths[0], caption)
                elif len(media_paths) == 1:
                    result = self.post_single_photo(channel_id, media_paths[0], caption)
                else:
                    result = self.post_media_group(channel_id, media_paths, caption)
                results[channel_id] = {"success": True, "result": result}
            except Exception as e:
                results[channel_id] = {"success": False, "error": str(e)}
        return results
