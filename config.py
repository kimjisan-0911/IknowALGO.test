import os
from dotenv import load_dotenv

# .env 파일 로드 (존재하는 경우)
load_dotenv()

class Config:
    # Flask 설정
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    
    # MySQL 설정
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = int(os.environ.get('DB_PORT') or 3306)
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'your_password'
    DB_NAME = os.environ.get('DB_NAME') or 'iknowalgo'
    
    # SQLAlchemy 설정
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }

config = Config() 