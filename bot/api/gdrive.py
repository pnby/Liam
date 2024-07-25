from datetime import timedelta, datetime, timezone
import pprint
import time
from typing import Any, Optional, final

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from bot import logger


@final
class GoogleDriveManager(object):
    _pp = pprint.PrettyPrinter(indent=4)
    _scopes: list[str]
    _sa_file_path: str
    _credentials: Any
    _service: Any

    def __init__(self, scopes: list[str], sa_file_path: str):
        self._scopes = scopes
        self._sa_file_path = sa_file_path
        self._credentials = service_account.Credentials.from_service_account_file(
            self._sa_file_path, scopes=self._scopes)
        self._service = build('drive', 'v3', credentials=self._credentials)

    def get_files(self, page_size: int = 10, fields: str = "nextPageToken, files(id, name, mimeType, parents, "
                                                           "createdTime, size)") -> Any:
        results = self._service.files().list(
            pageSize=page_size,
            fields=fields).execute()
        return results["files"]

    def get_folder(self, name: Optional[str] = None):
        files = self.get_files()
        for file in files:
            if name is None:
                if file["mimeType"] == "application/vnd.google-apps.folder":
                    return file
            else:
                if file["mimeType"] == "application/vnd.google-apps.folder" and file["name"] == name:
                    return file

    def clear_old_files(self, days: int = 2, application: str = "x-tar"):
        files = self.get_files(page_size=100)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        cutoff_date = now - timedelta(days=days)

        for file in files:
            created_time = datetime.strptime(file['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if created_time < cutoff_date and file['mimeType'] == f"application/{application}":
                self._service.files().delete(fileId=file['id']).execute()
                logger.info(f"Deleted file: {file['name']} created at {file['createdTime']}")

    def _upload_file(self, folder_id: str, filename: str, file_path: str) -> Any:
        media = MediaFileUpload(file_path, resumable=True)
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        r = self._service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return r

    def upload_file(self, folder_id: str, filename: str, file_path: str):
        logger.info("Starting file uploading")
        start_time = time.time()
        self._upload_file(folder_id, filename + ".tar", file_path)
        end_time = time.time()
        total = end_time - start_time
        logger.info(f"File uploading successfully ended for {total} secs")

    def get_pp(self):
        return self._pp
