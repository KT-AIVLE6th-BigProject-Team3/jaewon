from sqlalchemy.orm import Session, Query
from sqlalchemy import desc
from . import models, schemas
import datetime

# QnA 신규 글글 작성
def create_qna(db: Session, qna: schemas.QnaCreate):
    new_qna = models.Qna(writer_id=qna.writer_id, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content=qna.content, title=qna.title)
    db.add(new_qna)
    db.commit()
    db.refresh(new_qna)
    return new_qna

# QnA 목록 조회
def get_qna(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Qna).order_by(desc(models.Qna.qna_id)).offset(skip).limit(limit).all()

# 특정 QnA 게시글 조회
def get_qna_by_id(db: Session, qna_id: int):
    return db.query(models.Qna).filter(models.Qna.qna_id == qna_id).first()

# QnA 게시글 수정
def update_qna(db: Session, qna_id: int, qna: schemas.QnaUpdate):
    db_qna = db.query(models.Qna).filter(models.Qna.qna_id == qna_id).first()
    
    if db_qna is None:
        return None

    if qna.title:
        db_qna.title = qna.title
    if qna.content:
        db_qna.content = qna.content
        
    db.commit()
    db.refresh(db_qna)
    
    return db_qna

# QnA 게시글 답변
def answer_qna(db: Session, qna_id: int, qna: schemas.QnaUpdate):
    db_qna = db.query(models.Qna).filter(models.Qna.qna_id == qna_id).first()
    
    if db_qna is None:
        return None
    
    db_qna.answer_id = qna.answer_id
    db_qna.answer_content = qna.answer_content
        
    db.commit()
    db.refresh(db_qna)
    
    return db_qna

# QnA 게시글 삭제
def delete_qna(db: Session, qna_id: int):
    existing_qna = db.query(models.Qna).filter(models.Qna.qna_id == qna_id).first()
    if existing_qna:
        db.delete(existing_qna)
        db.commit()
    return existing_qna

