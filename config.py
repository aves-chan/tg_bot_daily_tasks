import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_PATH = f'postgresql://postgres:{str(os.getenv("DB_PASSWORD"))}@database:{str(os.getenv("DB_PORT"))}/tg_bot'
