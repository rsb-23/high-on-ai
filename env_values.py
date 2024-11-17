import os

if "CF_API_KEY" not in os.environ:
    from dotenv import load_dotenv  # noqa

    load_dotenv()

CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]
CF_API_KEY = os.environ["CF_API_KEY"]
SAVE_RESPONSE = os.environ.get("SAVE_RESPONSE", False)
