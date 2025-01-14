from pydantic import BaseModel
from typing import Optional

class NoticeBase(BaseModel):
    writer_id: str
    content: str
    title: str
    date: str

# 게시글 작성 요청 스키마
class NoticeCreate(NoticeBase):
    pass

# 게시글 수정 요청 스키마
class NoticeUpdate(BaseModel):
    content: str
    title: str

# 게시글 응답 스키마
class NoticeResponse(NoticeBase):
    notice_id: int

    class Config:
        orm_mode = True