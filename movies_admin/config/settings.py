import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = ["127.0.0.1"]

LOCALE_PATHS = ["movies/locale"]

include(
    "components/application_definition.py",
    "components/database.py",
    "components/default_primary_key_field_type.py",
    "components/internationalization.py",
    "components/middleware.py",
    "components/password_validadors.py",
    "components/static_files.py",
)
