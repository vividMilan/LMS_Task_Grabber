import os
from pathlib import Path
from urllib.parse import unquote

from playwright.sync_api import Error as PlaywrightError


def download_file(page, file_url: str, output_dir: str = "downloads") -> str | None:
    """Downloads a file using Playwright's authenticated browser session.

    Returns the saved local file path or None if the download fails.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Extract clean filename from URL (decodes %20 spaces and removes query params)
    raw_filename = file_url.split("/")[-1].split("?")[0]
    clean_filename = unquote(raw_filename)

    file_path = Path(output_dir) / clean_filename

    try:
        # page.request inherits session cookies automatically
        response = page.request.get(file_url)

        if response.status == 200:
            file_path.write_bytes(response.body())
            print(f"[+] Successfully downloaded: {file_path}")
            return str(file_path)

        print(f"[!] Failed to download. HTTP status: {response.status}")
    except PlaywrightError as e:
        print(f"[!] Error downloading {file_url}: {e}")

    return None
