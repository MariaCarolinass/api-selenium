import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:123@localhost:5432/bd")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
