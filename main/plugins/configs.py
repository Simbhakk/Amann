import os


class Config(object):
	API_ID = int(os.environ.get("API_ID", ''))
	API_HASH = os.environ.get("API_HASH",'')
	BOT_TOKEN = os.environ.get("BOT_TOKEN", '')
	BOT_USERNAME = os.environ.get("BOT_USERNAME", '')
	BOT_OWNER = int(os.environ.get("BOT_OWNER", ''))
	DATABASE_URL = os.environ.get("DATABASE_URL",'')
	LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ''))
	BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "1234567890").split())
	BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "-1001362659779").split()))
	