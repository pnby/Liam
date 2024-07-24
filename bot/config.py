from dotenv import load_dotenv
from envparse import env

load_dotenv()

BOT_TOKEN = env.str("BOT_TOKEN")
POSTGRES_URL = env.str("POSTGRES_URL", default="postgresql+asyncpg://postgres:1@postgres/postgres")
ADMIN_IDs = env.tuple("ADMIN_IDS")


SOURCE_DIR = env.str("SOURCE_DIR")
DESTINATION_DIR = env.str("DESTINATION_DIR")
SA_FILE_PATH = env.str("SA_FILE_PATH")

MYSQL_USER = env.str("MYSQL_USER")
MYSQL_PASS = env.str("MYSQL_PASS")

