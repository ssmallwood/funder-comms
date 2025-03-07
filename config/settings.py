"""Configuration settings for the Funder Communications Tool."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-3-opus-20240229")
