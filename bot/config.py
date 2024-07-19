from dotenv import load_dotenv
from envparse import env

load_dotenv()

BOT_TOKEN = env.str("BOT_TOKEN")
POSTGRES_URL = env.str("POSTGRES_URL", default="postgresql+asyncpg://postgres:pass@postgres_docker/bot")
