import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

def is_serverless_environment() -> bool:
    """Checks if the app is running in a serverless environment like Vercel/AWS Lambda."""
    return bool(
        os.environ.get('VERCEL') == '1'
        or os.environ.get('VERCEL_ENV')
        or os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
    )

def get_database_uri() -> str:
    """
    Resolves the database URI based on environment variables.
    - Uses DATABASE_URL, POSTGRES_URL, or SQLALCHEMY_DATABASE_URI if provided.
    - Automatically normalizes legacy 'postgres://' to 'postgresql://' for SQLAlchemy 1.4+ / 2.0+.
    - On Vercel / serverless, enforces that DATABASE_URL is set so data persists (refuses ephemeral /tmp).
    - In local development, falls back to the local SQLite database in instance/conference.db.
    """
    db_url = (
        os.environ.get('DATABASE_URL')
        or os.environ.get('POSTGRES_URL')
        or os.environ.get('SQLALCHEMY_DATABASE_URI')
    )

    if db_url:
        # Standardize postgres:// to postgresql:// for SQLAlchemy 2.0 compatibility
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return db_url

    if is_serverless_environment():
        raise RuntimeError(
            "DATABASE_URL environment variable is required on Vercel for persistent database storage (e.g., PostgreSQL). "
            "Serverless filesystems cannot persist local SQLite databases, and ephemeral /tmp storage must not be used. "
            "Please configure DATABASE_URL in your Vercel project environment variables."
        )

    return f"sqlite:///{BASE_DIR / 'instance' / 'conference.db'}"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'snpsu_bdtt_conf_2026_default_secret_key_8f7b3a9c')
    
    # Database: Environment-variable based in production, local SQLite in development
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'papers')
    SPEAKER_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'speakers')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    
    # Official Conference Branding
    CONFERENCE_NAME = "International Conference on Big Data Tools and Techniques (ICBDTT-2026)"
    CONFERENCE_ACRONYM = "ICBDTT-2026"
    CONFERENCE_BRAND_NAME = "ICBDTT-2026"
    CONFERENCE_THEME = "Big Data Tools and Techniques, Intelligent Computing & Scalable Analytics"
    HOST_INSTITUTION = "Sapthagiri NPS University (SNPSU)"
    HOST_LOCATION = "Bengaluru, Karnataka, India"
    HOST_CAMPUS = "Sapthagiri NPS University Campus, Chikkasandra, Hesaraghatta Main Road, Bengaluru, Karnataka 560057"
    VENUE_NAME = "Dr. APJ Abdul Kalam Auditorium, SNPSU Campus, Bengaluru, Karnataka, India"
    CONFERENCE_DATE = "20–21 November 2026"
    CONFERENCE_TIMING = "10:00 AM – 4:00 PM"
    CONFERENCE_EMAIL = "icbdtt@snpsu.edu.in"
    CONFERENCE_PHONE = "+91 (080) 2837 2800 / +91 94808 31234"
    REGISTRATION_FEE_PLACEHOLDER = "₹ 1,500 – ₹ 6,000 / $ 50 – $ 180"
