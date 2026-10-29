import keyring

SERVICE_NAME = "LMS Tracker"

def save_credentials(username: str, password: str) -> None:
    """Save LMS credentials to the operating system's credential store."""

    keyring.set_password(
        SERVICE_NAME,
        "username",
        username
    )

    keyring.set_password(
        SERVICE_NAME,
        username=username,
        password=password
    )

def save_lms_link(lms_link: str) -> None:
    """Save LMS link to OS credential store."""

    keyring.set_password(
        SERVICE_NAME,
        "lms_link",
        lms_link
    )

def get_credentials() -> str | None:
    """Get the saved LMS password."""

    username = keyring.get_password(
        SERVICE_NAME,
        "username",
    )

    password = keyring.get_password(
        SERVICE_NAME,
        username
    )

    if not username:
        return None, None

    return username, password

def get_lms_link() -> str | None:
    """Get the saved LMS link"""

    lms_link = keyring.get_password(
        SERVICE_NAME,
        "lms_link"
    )

    return lms_link

def delete_credentials() -> None:
    """Delete saved LMS credentials."""
    
    username = keyring.get_password(
        SERVICE_NAME,
        "username"
    )

    if username:
        try:
            keyring.delete_password(
                SERVICE_NAME,
                username,
            )

        except keyring.errors.PasswordDeleteError:
            pass

    try:
        keyring.delete_password(
            SERVICE_NAME,
            "username"
        )
    except keyring.errors.PasswordDeleteError:
        pass