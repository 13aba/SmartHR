
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class Config:
    UPLOAD_DIR: str = "../candidate_cv/"
    MODEL_NAME: str = "gpt-4.1-mini"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

candidate_config = Config()


job_config = Config()
job_config.UPLOAD_DIR = "../job_listing/"

