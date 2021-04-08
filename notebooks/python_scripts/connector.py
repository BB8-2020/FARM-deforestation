from sentinelhub import SHConfig
from dotenv import load_dotenv
import os

load_dotenv()
config = SHConfig()
config.sh_client_id = os.environ.get("SH_ID")
config.sh_client_secret = os.environ.get("SH_SECRET")

if config.sh_client_id == '' or config.sh_client_secret == '':
    print("Warning! To use Sentinel Hub Process API, please provide the credentials (client ID and client secret).")
else:
    print("Succefully connected!")