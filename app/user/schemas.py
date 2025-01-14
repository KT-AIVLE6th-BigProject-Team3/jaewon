from pydantic import BaseModel, EmailStr
from typing import Optional

# Define Pydantic Model for define user input and response data

class UserBase(BaseModel):
    userID: str

class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str
    password2: str
    role: str
    department: str
    
class UserLogin(UserBase):
    password: str
    
class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str]
    password2: Optional[str]
    role: Optional[str]
    department: Optional[str]
    
class UserResponse(UserBase):
    userID: str
    is_active: bool
    
    class Config:
        orm_mode = True