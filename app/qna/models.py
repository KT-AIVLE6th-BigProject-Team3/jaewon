from sqlalchemy import Column, Integer, String
from .database import Base

class Qna(Base):
    __tablename__ = "qna"

    qna_id = Column(Integer, primary_key=True, index=True) # 공지사항 번호
    writer_id = Column(String) # 작성자 고유번호
    date = Column(String) # Date, 작성일자
    content = Column(String) # 작성 내용
    title = Column(String) # 제목
    answer_id = Column(String, nullable=True) # 답변자(관리자) ID
    answer_content = Column(String, nullable=True) # 답변 내용용
    