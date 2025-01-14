from sqlalchemy.orm import Session
from .models import User
from passlib.context import CryptContext
from datetime import timezone
import datetime
# import datetime

# CryptContext 초기화
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해시화
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 사용자 생성
def create_user(db: Session, userID: str, name: str, email: str, password: str, role: str, department: str):
    now = datetime.datetime.now()
    user = User(userID=userID, name=name, email=email, password=hash_password(password), role=role, created_at=now.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at = now.strftime("%Y-%m-%d %H:%M:%S"), department=department)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 사용자 조회
def get_user_by_id(db: Session, userID: str):
    return db.query(User).filter(User.userID == userID).first()

# 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt로 해시된 비밀번호 비교
    return pwd_context.verify(plain_password, hashed_password)

# 로그인 검증
def verify_user_login(db: Session, userID: str, password: str):
    # 이메일로 사용자 조회
    user = get_user_by_id(db, userID)
    if not user:
        return None # 이메일이 존재하지 않으면 None 반환
    
    # 비밀번호 검증
    if not verify_password(password, user.password):
        return None
    
    return user

# 모든 사용자 조회
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

# 이슈사항
# (trapped) error reading bcrypt version
# Traceback (most recent call last):
#   File "C:\Users\User\anaconda3\envs\bp\Lib\site-packages\passlib\handlers\bcrypt.py", line 620, in _load_backend_mixin
#     version = _bcrypt.__about__.__version__
#               ^^^^^^^^^^^^^^^^^
# AttributeError: module 'bcrypt' has no attribute '__about__'
# 결론: 무시해도 되는지 여부 by ChatGPT 4o mini
# 단기적으로는: 비밀번호 암호화와 복호화가 정상적으로 이루어진다면, 이 오류는 큰 영향을 미치지 않으므로 일시적으로 무시할 수 있습니다.
# 장기적으로는: 해당 오류가 계속 발생하는 이유를 해결하는 것이 좋습니다. 최신 버전의 라이브러리를 사용하고 있다면, 해당 라이브러리의 버전 호환성 문제를 해결하는 것이 향후 안전합니다.