from pathlib import Path
from urllib.parse import unquote
import requests


def download_file(file_url: str, download_path: str = "downloads"):

    file_name = unquote(file_url.split("/")[-1].split("?")[0])
    save_path = Path(download_path) / file_name
    save_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(file_url, timeout=30)

    if response.status_code == 200:
        save_path.write_bytes(response.content)
        print(f"[+] Downloaded: {save_path}")
        return str(save_path)

    print(f"[!] Failed with status: {response.status_code}")
    return None
