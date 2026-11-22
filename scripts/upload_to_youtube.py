#!/usr/bin/env python3
"""Upload a video to YouTube and attach a thumbnail using the Data API.
Uses OAuth 2.0; the first run will open a browser to authorise."""
import os, json, base64, argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly"]

def get_service():
    """Return an authorized YouTube service instance."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Run the OAuth flow; this will open a browser window.
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload(video_path: str, title: str, description: str,
           tags: str, thumbnail_path: str, privacy: str = "private"):
    youtube = get_service()

    # 1️⃣ Insert the video
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [t.strip() for t in tags.split(",")],
            "categoryId": "22",            # People & Blogs; change to "27" for Education
            "defaultLanguage": "en"
        },
        "status": {"privacyStatus": privacy}
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    video_id = response["id"]
    print(f"✅ Video uploaded (id={video_id})")

    # 2️⃣ Set the thumbnail
    with open(thumbnail_path, "rb") as f:
        thumb_data = f.read()
    youtube.thumbnails().set(videoId=video_id, image=base64.b64encode(thumb_data).decode()).execute()
    print(f"✅ Thumbnail set for video {video_id}")

    # Optionally publish:
    # youtube.videos().update(part="status", body={"status": {"privacyStatus": "public"}}, id=video_id).execute()

    return video_id


def main():
    parser = argparse.ArgumentParser(description="Upload an Ayurvedic video to YouTube")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", required=True, help="Video description")
    parser.add_argument("--tags", required=True, help="Comma‑separated tag list")
    parser.add_argument("--video", required=True, help="Path to MP4 video")
    parser.add_argument("--thumbnail", required=True, help="Path to thumbnail JPEG")
    parser.add_argument("--privacy", default="private", choices=["private", "public", "unlisted"],
                        help="Privacy status (default: private)")
    args = parser.parse_args()

    upload(args.video, args.title, args.description, args.tags, args.thumbnail, args.privacy)


if __name__ == "__main__":
    main()