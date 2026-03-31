"""
Module for publishing to Facebook Page and Instagram via Meta Graph API.
Supports: single photo, carousel, video (Reels on IG).

IMPORTANT NOTE: Instagram requires publicly accessible URLs for images.
This module uploads photos to Facebook (unpublished) to obtain a public URL,
which is then used for Instagram publishing.
"""
import requests
import time
import os
from typing import Optional


class MetaPoster:
    """Handles publishing content to Facebook Pages and Instagram via Graph API."""

    BASE_URL = "https://graph.facebook.com/v21.0"

    def __init__(self, page_access_token: str, page_id: str,
                 instagram_account_id: str = ""):
        """
        Initialize the Meta poster.

        Args:
            page_access_token: Facebook Page Access Token.
            page_id: Facebook Page ID.
            instagram_account_id: Instagram Professional Account ID (optional).
        """
        self.token = page_access_token
        self.page_id = page_id
        self.ig_account_id = instagram_account_id

    # ----------------------------------------------------------------
    # FACEBOOK
    # ----------------------------------------------------------------
    def fb_post_single_photo(self, photo_path: str, message: str) -> dict:
        """Publish a single photo to the Facebook Page."""
        url = f"{self.BASE_URL}/{self.page_id}/photos"
        with open(photo_path, "rb") as photo:
            resp = requests.post(
                url,
                data={"message": message, "access_token": self.token},
                files={"source": photo},
                timeout=120,
            )
        resp.raise_for_status()
        return resp.json()

    def fb_post_video(self, video_path: str, description: str) -> dict:
        """Publish a video to the Facebook Page."""
        url = f"{self.BASE_URL}/{self.page_id}/videos"
        with open(video_path, "rb") as video:
            resp = requests.post(
                url,
                data={"description": description, "access_token": self.token},
                files={"source": video},
                timeout=300,
            )
        resp.raise_for_status()
        return resp.json()

    def fb_post_carousel(self, photo_paths: list[str], message: str) -> dict:
        """
        Publish a carousel to Facebook (multi-photo post).
        Step 1: Upload each photo as 'unpublished'.
        Step 2: Create a post that groups them together.
        """
        photo_ids = []
        for path in photo_paths:
            url = f"{self.BASE_URL}/{self.page_id}/photos"
            with open(path, "rb") as photo:
                resp = requests.post(
                    url,
                    data={
                        "published": "false",
                        "access_token": self.token,
                    },
                    files={"source": photo},
                    timeout=120,
                )
            resp.raise_for_status()
            photo_ids.append(resp.json()["id"])

        # Create the post with all photos attached
        url = f"{self.BASE_URL}/{self.page_id}/feed"
        data = {
            "message": message,
            "access_token": self.token,
        }
        for i, pid in enumerate(photo_ids):
            data[f"attached_media[{i}]"] = f'{{"media_fbid":"{pid}"}}'

        resp = requests.post(url, data=data, timeout=60)
        resp.raise_for_status()
        return resp.json()

    # ----------------------------------------------------------------
    # INSTAGRAM
    # ----------------------------------------------------------------
    def _upload_photo_to_fb_and_get_url(self, photo_path: str) -> str:
        """
        Upload a photo to Facebook (unpublished) to obtain a public URL
        for use with the Instagram API.
        """
        url = f"{self.BASE_URL}/{self.page_id}/photos"
        with open(photo_path, "rb") as photo:
            resp = requests.post(
                url,
                data={"published": "false", "access_token": self.token},
                files={"source": photo},
                timeout=120,
            )
        resp.raise_for_status()
        photo_id = resp.json()["id"]

        # Get the image URL
        url = f"{self.BASE_URL}/{photo_id}?fields=images&access_token={self.token}"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        images = resp.json().get("images", [])
        if images:
            return images[0]["source"]
        raise Exception("Unable to retrieve photo URL from Facebook")

    def ig_post_single_photo(self, photo_path: str, caption: str) -> dict:
        """Publish a single photo to Instagram."""
        if not self.ig_account_id:
            return {"error": "Instagram Account ID not configured"}

        image_url = self._upload_photo_to_fb_and_get_url(photo_path)

        # Step 1: Create the media container
        url = f"{self.BASE_URL}/{self.ig_account_id}/media"
        resp = requests.post(url, data={
            "image_url": image_url,
            "caption": caption,
            "access_token": self.token,
        }, timeout=60)
        resp.raise_for_status()
        creation_id = resp.json()["id"]

        # Step 2: Publish
        return self._ig_publish(creation_id)

    def ig_post_carousel(self, photo_paths: list[str], caption: str) -> dict:
        """Publish a carousel to Instagram."""
        if not self.ig_account_id:
            return {"error": "Instagram Account ID not configured"}

        # Step 1: Create a container for each image
        children_ids = []
        for path in photo_paths:
            image_url = self._upload_photo_to_fb_and_get_url(path)
            url = f"{self.BASE_URL}/{self.ig_account_id}/media"
            resp = requests.post(url, data={
                "image_url": image_url,
                "is_carousel_item": "true",
                "access_token": self.token,
            }, timeout=60)
            resp.raise_for_status()
            children_ids.append(resp.json()["id"])

        # Step 2: Create the carousel container
        url = f"{self.BASE_URL}/{self.ig_account_id}/media"
        resp = requests.post(url, data={
            "media_type": "CAROUSEL",
            "caption": caption,
            "children": ",".join(children_ids),
            "access_token": self.token,
        }, timeout=60)
        resp.raise_for_status()
        creation_id = resp.json()["id"]

        # Step 3: Publish
        return self._ig_publish(creation_id)

    def ig_post_video(self, video_path: str, caption: str,
                      video_url: str = "") -> dict:
        """
        Publish a video/reel to Instagram.
        NOTE: Instagram requires a public URL for videos.
        You must provide video_url (e.g., via upload to a hosting service).
        """
        if not self.ig_account_id:
            return {"error": "Instagram Account ID not configured"}
        if not video_url:
            return {"error": "Instagram requires a public URL for videos. "
                            "Upload it to a hosting service (e.g., your Shopify site) and pass the URL."}

        url = f"{self.BASE_URL}/{self.ig_account_id}/media"
        resp = requests.post(url, data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": self.token,
        }, timeout=60)
        resp.raise_for_status()
        creation_id = resp.json()["id"]

        # Wait for video processing to complete
        self._wait_for_ig_media(creation_id)
        return self._ig_publish(creation_id)

    def _ig_publish(self, creation_id: str) -> dict:
        """Publish a media container to Instagram."""
        url = f"{self.BASE_URL}/{self.ig_account_id}/media_publish"
        resp = requests.post(url, data={
            "creation_id": creation_id,
            "access_token": self.token,
        }, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def _wait_for_ig_media(self, creation_id: str, max_wait: int = 60):
        """Wait for Instagram to finish processing the media."""
        url = f"{self.BASE_URL}/{creation_id}?fields=status_code&access_token={self.token}"
        for _ in range(max_wait // 5):
            resp = requests.get(url, timeout=30)
            data = resp.json()
            status = data.get("status_code", "")
            if status == "FINISHED":
                return
            if status == "ERROR":
                raise Exception(f"Instagram processing error: {data}")
            time.sleep(5)
        raise Exception("Timeout waiting for Instagram media processing")

    # ----------------------------------------------------------------
    # UNIFIED METHOD
    # ----------------------------------------------------------------
    def publish(self, media_paths: list[str], caption: str,
                is_video: bool = False, video_url: str = "") -> dict:
        """
        Publish to both Facebook and Instagram.

        Returns:
            Dictionary with 'facebook' and 'instagram' results.
        """
        results = {"facebook": {}, "instagram": {}}

        # --- Facebook ---
        try:
            if is_video:
                results["facebook"] = {
                    "success": True,
                    "result": self.fb_post_video(media_paths[0], caption),
                }
            elif len(media_paths) == 1:
                results["facebook"] = {
                    "success": True,
                    "result": self.fb_post_single_photo(media_paths[0], caption),
                }
            else:
                results["facebook"] = {
                    "success": True,
                    "result": self.fb_post_carousel(media_paths, caption),
                }
        except Exception as e:
            results["facebook"] = {"success": False, "error": str(e)}

        # --- Instagram ---
        if self.ig_account_id:
            try:
                if is_video:
                    results["instagram"] = {
                        "success": True,
                        "result": self.ig_post_video(media_paths[0], caption, video_url),
                    }
                elif len(media_paths) == 1:
                    results["instagram"] = {
                        "success": True,
                        "result": self.ig_post_single_photo(media_paths[0], caption),
                    }
                else:
                    results["instagram"] = {
                        "success": True,
                        "result": self.ig_post_carousel(media_paths, caption),
                    }
            except Exception as e:
                results["instagram"] = {"success": False, "error": str(e)}

        return results
