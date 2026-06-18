import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
ALERT_THRESHOLD = int(os.getenv("ALERT_THRESHOLD", "100000"))

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

DEFAULT_ANALYST = os.getenv("DEFAULT_ANALYST")
DEFAULT_EXECUTIVE = os.getenv("DEFAULT_EXECUTIVE")