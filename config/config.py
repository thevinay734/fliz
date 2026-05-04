import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://dev.fliz.com.sa/")
API_BASE_URL = os.getenv("API_BASE_URL", "https://dev.api.fliz.com.sa/")
