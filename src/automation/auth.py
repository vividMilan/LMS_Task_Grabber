def login(page, username, password, url):
    """Logs into OUSL LMS via IAM."""
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print("Opened login page.")

        page.get_by_role("link", name="IAM OUSL LMS USER").click()
        print("Redirecting..")

        page.wait_for_selector('input[name="username"]', timeout=60000)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('input[type="submit"]')
        print("Submitted login credentials.")

        page.wait_for_selector('div[role="listitem"]', timeout=60000)
        print("Logged in successfully!")

    except TimeoutError as e:
        print("Timeout or login failed:", e)
        return False
    except Exception as e:
        print("Login error:", e)
        return False

    return True