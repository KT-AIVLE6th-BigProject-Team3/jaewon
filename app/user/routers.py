from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from ..main import create_access_token
from fastapi.responses import JSONResponse
import jwt
from jose import JWTError
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv(dotenv_path="app\config.env")

# # 데이터베이스와 연결을 설정
models.Base.metadata.create_all(bind=database.engine)

# # 의존성 주입 : 요청마다 데이터베이스 세션을 생성
# 데이터베이스 세션 생성 및 반환
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/sign_in') # Log_in
def log_in(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # userID이나 password 입력 칸 중 하나가 공백일 경우
    if (user.userID == "" or user.password == ""):
        raise HTTPException(status_code=400, detail="ID와 비밀번호를 입력해 주세요.")
    
    usr = crud.verify_user_login(db, user.userID, user.password) # user와 혼동되지 않도록 usr로 지정
    
    #존재하지 않는 userID이거나 password가 일치하지 않을 경우
    if usr is None:
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 잘못되었습니다.")
    
    # 토큰을 발급하여 반환
    access_token = create_access_token(data={"sub": usr.userID})
    return {"message": f"{usr.name}님 환영합니다!", "user": usr.name, "userID": usr.userID, "access_token": access_token} # token 포함 반환

    #else (something error?)
    # return something undefined error, try later

@router.post('/sign_up', status_code=status.HTTP_201_CREATED) # Sign up new account
def create_account(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # if something empty in input values
    if (user.userID == "" or user.name == "" or user.email == "" or user.password == "" or user.password2 == "" or user.role == "" or user.department == ""):
        raise HTTPException(status_code=400, detail="빈 칸 없이 모든 사용자 정보를 입력하여 주세요.")
    # if (primary key) email already exist in db
    existing_user = crud.get_user_by_id(db, user.userID)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"입력하신 이메일 {user.userID}은 이미 등록된 ID입니다.")
    # if password != password2
    elif (user.password != user.password2):
        raise HTTPException(status_code=400, detail="비밀번호 재입력이 올바르지 않습니다. Caps Lock이 켜져있는지 확인하시고 다시 입력해 주세요.")
    # else --> create account at db and back to login page
    else:
        return crud.create_user(db, user.userID, user.name, user.email, user.password, user.role, user.department)
    
# Log In / Out의 사용자 인증 정보 저장 방법으로는 JWT 토큰 사용 or FastAPI Session을 이용하는 두 가지 방안
# Log out은 클라이언트 측에서 인증 정보를 지워야 함. JWT 방식일 경우 JWT 토큰 삭제 or 토큰 제거.
@router.get('/sign_out')
def log_out(response: Response):
    # 클라이언트에서 JWT 토큰을 삭제하는 방식으로 로그아웃 처리
    
    response.delete_cookie("access_token")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "성공적으로 로그아웃되었습니다."})