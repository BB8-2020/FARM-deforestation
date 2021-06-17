"""Helper file to download onedrive folder(s)/file(s) locally."""
import os

from dotenv import load_dotenv
from onedrivesdk import get_default_client
from onedrivesdk.helpers import GetAuthCodeServer
from onedrivesdk.request.one_drive_client import OneDriveClient


class OneDriveHelper:
    """OneDriveHelper class to connect to onderive and download from it."""

    def __init__(self, root_folder: str = "bb8", client: OneDriveClient = None):
        """Open format and save the locations.

        Parameters
        ----------
        root_folder
            The root folder of your onderive directory.
        """
        self.root_folder = root_folder
        self.client = self.connect() if client is None else client

    def connect(self) -> OneDriveClient:
        """Authenticate into onderive using the enviroment variables and creating a new client.

        Returns
        -------
        client
            The authenticated OneDrive client.
        """
        load_dotenv()
        client_id, client_secret = os.environ.get("OD_ID"), os.environ.get("OD_SECRET")

        redirect_uri = "http://localhost:8080/"
        scopes = ["wl.signin", "wl.offline_access", "onedrive.readwrite"]
        client = get_default_client(client_id=client_id, scopes=scopes)
        auth_url = client.auth_provider.get_auth_url(redirect_uri)

        code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
        client.auth_provider.authenticate(code, redirect_uri, client_secret)
        return client

    def download_file(self, file_path: str, download_path: str):
        """Download a single file from a file path to a local download path.

        Parameters
        ----------
        file_path
            The onderive file path from the root folder.

        download_path
            The local file path to save the file.
        """
        folder_path = "/".join(download_path.split("/")[:-1])
        os.makedirs(folder_path, exist_ok=True)
        self.client.item(drive="me", path=f"{self.root_folder}/{file_path}").download(
            download_path
        )

    def download(self, path: str, prefix: str = "."):
        """Download a folder or file given a onedrive path and prefix for the relative download path.

        Parameters
        ----------
        path
            The onderive path to a file or folder relative to the root folder.

        prefix
            The prefix that gets added to the download path.
        """
        folders = self.client.item(
            drive="me", path=f"{self.root_folder}/{path}"
        ).children.get()
        for folder in folders:
            self.download(f"{path}/{folder.name}", prefix)
        if len(folders) == 0:
            self.download_file(path, f"{prefix}/{path}")
