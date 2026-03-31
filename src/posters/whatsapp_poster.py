"""
Module for publishing to WhatsApp Business groups via Cloud API.
Supports: single photo, video, and text with media.

NOTE: The WhatsApp Groups API requires:
- A verified Meta Business account
- A phone number registered on the Cloud API platform
- Groups must be created/managed via API
"""
import requests
import os
from typing import Optional


class WhatsAppPoster:
    """Handles publishing content to WhatsApp groups via Cloud API."""

    BASE_URL = "https://graph.facebook.com/v21.0"

    def __init__(self, token: str, phone_number_id: str, group_ids: list[str]):
        """
        Initialize the WhatsApp poster.

        Args:
            token: WhatsApp Cloud API access token.
            phone_number_id: The registered phone number ID.
            group_ids: List of WhatsApp group IDs.
        """
        self.token = token
        self.phone_number_id = phone_number_id
        self.group_ids = group_ids
        self.headers = {
            "Authorization": f"Bearer {self.token}",
        }

    def _upload_media(self, file_path: str) -> str:
        """Upload a media file to WhatsApp and return the media_id."""
        url = f"{self.BASE_URL}/{self.phone_number_id}/media"

        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp",
            ".mp4": "video/mp4", ".3gp": "video/3gpp",
        }
        mime_type = mime_types.get(ext, "application/octet-stream")

        with open(file_path, "rb") as f:
            resp = requests.post(
                url,
                headers=self.headers,
                files={"file": (os.path.basename(file_path), f, mime_type)},
                data={"messaging_product": "whatsapp"},
                timeout=120,
            )
        resp.raise_for_status()
        return resp.json()["id"]

    def _send_to_group(self, group_id: str, message_data: dict) -> dict:
        """Send a message to a WhatsApp group."""
        url = f"{self.BASE_URL}/{self.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "group",
            "to": group_id,
            **message_data,
        }
        resp = requests.post(url, headers={**self.headers, "Content-Type": "application/json"},
                             json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def post_image(self, group_id: str, image_path: str, caption: str) -> dict:
        """Send a single image with caption."""
        media_id = self._upload_media(image_path)
        return self._send_to_group(group_id, {
            "type": "image",
            "image": {"id": media_id, "caption": caption},
        })

    def post_video(self, group_id: str, video_path: str, caption: str) -> dict:
        """Send a video with caption."""
        media_id = self._upload_media(video_path)
        return self._send_to_group(group_id, {
            "type": "video",
            "video": {"id": media_id, "caption": caption},
        })

    def post_text(self, group_id: str, text: str) -> dict:
        """Send a text-only message."""
        return self._send_to_group(group_id, {
            "type": "text",
            "text": {"body": text},
        })

    def publish(self, media_paths: list[str], caption: str,
                is_video: bool = False) -> dict:
        """
        Publish to all configured groups.

        For WhatsApp: if there are multiple photos, the first one is sent
        with the caption and the rest are sent without (WhatsApp doesn't
        have a native "carousel" like Telegram, but photos sent in rapid
        succession create a similar effect).

        Returns:
            Dictionary mapping group IDs to their results.
        """
        results = {}
        for group_id in self.group_ids:
            try:
                if is_video:
                    result = self.post_video(group_id, media_paths[0], caption)
                    results[group_id] = {"success": True, "result": result}
                elif len(media_paths) == 1:
                    result = self.post_image(group_id, media_paths[0], caption)
                    results[group_id] = {"success": True, "result": result}
                else:
                    # First photo with caption, the rest without
                    group_results = []
                    for i, path in enumerate(media_paths):
                        cap = caption if i == 0 else ""
                        r = self.post_image(group_id, path, cap)
                        group_results.append(r)
                    results[group_id] = {"success": True, "result": group_results}
            except Exception as e:
                results[group_id] = {"success": False, "error": str(e)}
        return results
