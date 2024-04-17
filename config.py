from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGODB_URI = os.getenv('MONGODB_URI')
REQUIRED_CHANNEL_IDS = os.getenv("TELEGRAM_REQUIRED_CHANNELS").split(",")
