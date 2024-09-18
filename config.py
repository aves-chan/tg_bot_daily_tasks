import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

REDIS_HOST = 'redis'
DB_HOST = 'database'
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_PATH = f'postgresql://postgres:{str(os.getenv("DB_PASSWORD"))}@{DB_HOST}:{str(os.getenv("DB_PORT"))}/tg_bot'
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_PORT = os.getenv('REDIS_PORT')
