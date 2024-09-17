import os
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT')
}

CHANNEL_ID = os.getenv('CHANNEL_ID')
MAX_VIDEOS_PER_CHANNEL = int(os.getenv('MAX_VIDEOS_PER_CHANNEL'))
MAX_COMMENTS_PER_VIDEO = int(os.getenv('MAX_COMMENTS_PER_VIDEO'))
