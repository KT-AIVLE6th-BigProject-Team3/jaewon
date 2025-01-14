from sqlalchemy import Column, Integer, String, Enum
from .database import Base
import enum

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "user"
    # id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, index=True)
    # email = Column(String, unique=True, index=True)
    # password = Column(String)
    
    userID = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    password = Column(String) # hashed_password
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(String)
    updated_at = Column(String)
    department = Column(String, nullable=False)
    
# 최종 모델
# 사번(PK) / 이름 / 전화번호 / 이메일 / 비밀번호 / 비밀번호 확인 / 소속 부서