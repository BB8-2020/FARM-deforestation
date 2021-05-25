"""OS library used for file and folder operations."""
import os

import onedrivesdk
from dotenv import load_dotenv
from onedrivesdk.helpers import GetAuthCodeServer


class OneDriveHelper:
    """OneDriveHelper class to connect on creation and used to download."""

    def __init__(self, root_folder="bb8"):
        self.root_folder = root_folder
        self.client = self.connect()

    def connect(self):
        """Login and connects to your onedrive."""
        load_dotenv()
        client_id, client_secret = os.environ.get("OD_ID"), os.environ.get("OD_SECRET")

        redirect_uri = "http://localhost:8080/"
        scopes = ["wl.signin", "wl.offline_access", "onedrive.readwrite"]
        client = onedrivesdk.get_default_client(client_id=client_id, scopes=scopes)
        auth_url = client.auth_provider.get_auth_url(redirect_uri)

        code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
        client.auth_provider.authenticate(code, redirect_uri, client_secret)
        return client

    def download_file(self, file_path, download_path):
        """Download a single file from a file path to a local download path."""
        folder_path = "/".join(download_path.split("/")[:-1])
        os.makedirs(folder_path, exist_ok=True)
        self.client.item(drive="me", path=f"{self.root_folder}/{file_path}").download(
            download_path
        )

    def download(self, path, prefix="."):
        """Download a folder or file given a onedrive path and prefix for the relative download path."""
        folders = self.client.item(
            drive="me", path=f"{self.root_folder}/{path}"
        ).children.get()
        for folder in folders:
            self.download(f"{path}/{folder.name}", prefix)
        if len(folders) == 0:
            self.download_file(path, f"{prefix}/{path}")
