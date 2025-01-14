from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 URL 설정
DATABASE_URL = "sqlite:///./bigproject.db"

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스 세션 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델의 기본 클래스
Base = declarative_base()