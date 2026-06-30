from dotenv import load_dotenv
import os

load_dotenv()


def get_credentials():
    credentials = {
        "client_id": os.getenv("LWA_CLIENT_ID"),
        "client_secret": os.getenv("LWA_CLIENT_SECRET"),
        "refresh_token": os.getenv("REFRESH_TOKEN"),
        "marketplace_id": os.getenv("MARKETPLACE_ID"),
    }

    missing = [k for k, v in credentials.items() if not v]

    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")

    return credentials