import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
from dotenv import load_dotenv
import os


root_folder = 'bb8'

def connect():
    load_dotenv()
    client_id, client_secret = os.environ.get("OD_ID"), os.environ.get("OD_SECRET")

    redirect_uri = 'http://localhost:8080/'
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
    client = onedrivesdk.get_default_client(client_id=client_id, scopes=scopes)
    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
    client.auth_provider.authenticate(code, redirect_uri, client_secret)
    return client


def download_file(file_path):
    folder_path = '/'.join(file_path.split('/')[:-1])
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    client.item(drive='me', path=f'{root_folder}/{file_path}').download(file_path)


def download(folder_path):
    folders = client.item(drive='me', path=f'{root_folder}/{folder_path}').children.get()
    for folder in folders:
        download(f'{folder_path}/{folder.name}')
    if len(folders) == 0:
        download_file(folder_path)


client = connect()
