"""Test functions to check if the onderive helpers runs correctly."""
from unittest.mock import patch

import onedrivesdk

from python.helpers.onedrive import OneDriveHelper


@patch("onedrivesdk.HttpProvider")
@patch("onedrivesdk.AuthProvider")
def test_download(MockHttpProvider, MockAuthProvider):
    """Download a single fake file and test if the generated urls are correct.

    Parameters
    ----------
    MockHttpProvider
        A mock for the OneDrive http provider.

    MockAuthProvider
        A mock for the OneDrive authentication provider.
    """
    path = "./path-to-file/file.txt"

    client = onedrivesdk.OneDriveClient(
        "onedrive-url/", MockHttpProvider, MockAuthProvider
    )
    one_drive_helper = OneDriveHelper(client=client)
    one_drive_helper.download_file("file.txt", path)

    assert client.http_provider.download.call_args[0][2] == path
    assert (
        client.http_provider.download.call_args[0][1]
        == f"onedrive-url/drives/me/root:/{one_drive_helper.root_folder}/file.txt:/content"
    )
