#!/usr/bin/env python3
"""One‑time OAuth flow to create/refresh token.json for YouTube uploads."""
import os, json, sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Ensure client_secret.json is present in the working directory
    if not os.path.exists("client_secret.json"):
        sys.exit("❌ client_secret.json not found. Download it from Google Cloud Console.")
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials so future runs can reuse them
    with open("token.json", "w") as f:
        f.write(creds.to_json())
    print("✅ OAuth token saved to token.json")
    # Build a quick test service (optional)
    # service = build("youtube", "v3", credentials=creds)
    # print("Service created successfully.")


if __name__ == "__main__":
    main()