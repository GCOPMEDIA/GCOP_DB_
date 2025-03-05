from django.core.files.storage import Storage
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

import io

class GoogleDriveStorage(Storage):
    def __init__(self):
        self.credentials = Credentials.from_service_account_file("credentials.json")
        self.service = build('drive', 'v3', credentials=self.credentials)

    def exists(self, name):
        """Check if a file exists in Google Drive."""
        query = f"name = '{name}' and trashed = false"
        response = self.service.files().list(q=query, fields="files(id)").execute()
        return bool(response.get('files', []))  # Returns True if file exists

    def save(self, name, content, max_length=None):
        """Upload file to Google Drive (fixing max_length issue)."""
        file_metadata = {'name': name}
        media = MediaIoBaseUpload(io.BytesIO(content.read()), mimetype=content.content_type)
        file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return file.get("id")  # Return the file ID

    def url(self, name):
        """Return the URL for the uploaded file."""
        query = f"name = '{name}' and trashed = false"
        response = self.service.files().list(q=query, fields="files(id, webViewLink)").execute()
        files = response.get("files", [])
        return files[0]["webViewLink"] if files else None  # Return the first file's link if found
