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

    print("Credentials saved")

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