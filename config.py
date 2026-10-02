import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'snpsu_bdtt_conf_2026_default_secret_key_8f7b3a9c')
    
    # Database: SQLite for development, can easily be switched to PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{BASE_DIR / 'instance' / 'conference.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'papers')
    SPEAKER_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'speakers')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    
    # Official Conference Branding
    CONFERENCE_NAME = "National Conference in Emerging Trends of Big Data Engineering 2.6"
    CONFERENCE_ACRONYM = "Saptha DataZen 2.6"
    CONFERENCE_BRAND_NAME = "Saptha DataZen 2.6"
    CONFERENCE_THEME = "Emerging Trends in Big Data Engineering & Intelligent Computing Systems"
    HOST_INSTITUTION = "Sapthagiri NPS University"
    HOST_LOCATION = "Bangalore, Karnataka, India"
    HOST_CAMPUS = "Sapthagiri NPS University Campus, Chikkasandra, Hesaraghatta Main Road, Bangalore, Karnataka 560057"
    VENUE_NAME = "C Block, 1st Floor, Auditorium, Sapthagiri NPS University, Bangalore"
    CONFERENCE_DATE = "08th August 2026"
    CONFERENCE_EMAIL = "datazen@snpsu.edu.in"
    CONFERENCE_PHONE = "+91 (080) 2837 2800 / +91 94808 31234"
    REGISTRATION_FEE_PLACEHOLDER = "₹ 500 – ₹ 2,500"
