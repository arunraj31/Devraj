import os
from os import getenv


API_ID = int(os.environ.get("API_ID"))


API_HASH = os.environ.get("API_HASH")


BOT_TOKEN = os.environ.get("BOT_TOKEN")

OWNER_ID = list(
    map(int, getenv("OWNER_ID", "6844821478").split())
) 

HEROKU_API = os.environ.get("HEROKU_API")

MONGO_URL = os.environ.get("MONGO_URL")

LOGGER_ID = int(getenv("LOGGER_ID", "-1002113460681"))
