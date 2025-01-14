from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import datetime
from datetime import timezone
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from .user import database as user_database
# import sys
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
load_dotenv(dotenv_path="app\config.env") # 현재 디렉토리에서 config.env 파일을 찾아 로드함. 여기 명시된 변수는 프로세스 환경 변수로 설정됨.

# # 의존성 주입 : 요청마다 데이터베이스 세션을 생성
# 데이터베이스 세션 생성 및 반환
def get_db():
    db = user_database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # JWT 서명에 사용될 Secret Key 생성
# SECRET_KEY = "your_secret_key" # 이 값은 환경 변수 등으로 관리 권장 by GPT
# ALGORITHM =  "HS256" # 알고리즘 : HMAC-SHA256
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 토큰 만료 시간(분)

# JWT 토큰 발급 함수
def create_access_token(data: dict, expires_delta: datetime.timedelta = datetime.timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)))):
    to_encode = data.copy()
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    if not secret_key or not algorithm:
        raise ValueError("SECRET KEY or ALGORITHM not set in environment variables")
    expire = datetime.datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

##    사용자 정보 DB 라우터
from .user.models import Base as user_base
from .user.routers import router as user_router
# user router 등록
user_base.metadata.create_all(bind=user_database.engine)
app.include_router(user_router, prefix="", tags=["User"])

# 유저 정보 추출 함수
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(user_router.models.User).filter(user_router.models.User.userId == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed")


@app.get('/')
def read_root(token: str = Depends(oauth2_scheme)):
    # PLAN = Session에 사용자가 없다면 LOG IN PAGE 
    # PLAN = Session에 사용자가 있다면 main 페이지로
    return {'hello' : 'world!'}



##    공지사항 게시판 라우터
from .notice.models import Base as notice_base
from .notice.routers import router as notice_router
from .notice import database as notice_database
# notice router 등록
notice_base.metadata.create_all(bind=notice_database.engine)
app.include_router(notice_router, prefix="/board", tags=["Notice"])

##    QnA 게시판 라우터
from .qna.models import Base as qna_base
from .qna.routers import router as qna_router
from .qna import database as qna_database
# QnA router 등록
qna_base.metadata.create_all(bind=qna_database.engine)
app.include_router(qna_router, prefix="/board", tags=["QnA"])