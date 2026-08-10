from playwright.sync_api import sync_playwright


def launch_browser():
    """Launches the browser and returns the page object."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    return p, browser, page