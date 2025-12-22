from pathlib import Path
from dotenv import load_dotenv
import os

ADMIN_IDS = [849074459]

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "data" / "images"
BOOK_FILE_PATH = BASE_DIR / 'data' / 'book.pdf'

load_dotenv(BASE_DIR / '.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
PAY_URL = os.getenv('PAY_URL')

DB_PATH = BASE_DIR / 'data' / 'bot.db'

if BOT_TOKEN is None:
    raise RuntimeError('BOT_TOKEN is not set in .env')

if PAY_URL is None:
    raise RuntimeError('PAY_URL is not set in .env')

if not BOOK_FILE_PATH.exists():
    raise RuntimeError(f'Book file not found at {BOOK_FILE_PATH}')