import os
from pathlib import Path

from dotenv import load_dotenv


# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv(BASE_DIR / ".env")


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# --------------------------------------------------
# PROJECT DIRECTORIES
# --------------------------------------------------

UPLOAD_DIR = BASE_DIR / "uploads"

OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR = BASE_DIR / "data"

CHROMA_DIR = DATA_DIR / "chroma"


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASE_PATH = DATA_DIR / "meetings.db"


# --------------------------------------------------
# CREATE DIRECTORIES
# --------------------------------------------------

UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR.mkdir(exist_ok=True)

DATA_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# VALIDATE API KEY
# --------------------------------------------------

if not OPENROUTER_API_KEY:

    print(
        "WARNING: OPENROUTER_API_KEY "
        "is not configured."
    )