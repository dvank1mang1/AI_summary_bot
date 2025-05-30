import os
from dotenv import load_dotenv

load_dotenv() 

BOT_TOKEN = os.getenv("BOT_TOKEN")

DEFAULT_LANGUAGE = "ru"
DEFAULT_FREQ = "daily"
DEFAULT_SIZE = "medium"
