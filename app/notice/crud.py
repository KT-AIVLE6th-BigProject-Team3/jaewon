from sqlalchemy.orm import Session, Query
from sqlalchemy import desc
from . import models, schemas
import datetime

# 공지사항 작성
def create_notice(db: Session, notice: schemas.NoticeCreate):
    new_notice = models.Notice(writer_id=notice.writer_id, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content=notice.content, title=notice.title)
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice

# 공자사항 목록 조회
def get_notices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Notice).order_by(desc(models.Notice.notice_id)).offset(skip).limit(limit).all()

# 특정 게시글 조회
def get_notice_by_id(db: Session, notice_id: int):
    return db.query(models.Notice).filter(models.Notice.notice_id == notice_id).first()

# 게시글 수정
def update_notice(db: Session, notice_id: int, notice: schemas.NoticeUpdate):
    db_notice = db.query(models.Notice).filter(models.Notice.notice_id == notice_id).first()
    
    if db_notice is None:
        return None

    if notice.title:
        db_notice.title = notice.title
    if notice.content:
        db_notice.content = notice.content
    # notice.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # <- 게시글 수정시 수정 시간으로 적용할거면 넣는데 주석 풀면 500에러
        
    db.commit()
    db.refresh(db_notice)
    
    return db_notice
    
    # existing_notice = db.query(models.Notice).filter(models.Notice.notice_id == notice_id)
    # if existing_notice:
    #     existing_notice.content = notice.content
    #     existing_notice.title = notice.title
    #     db.commit()
    #     db.refresh(existing_notice)
    # return existing_notice

# 게시글 삭제
def delete_notice(db: Session, notice_id: int):
    existing_notice = db.query(models.Notice).filter(models.Notice.notice_id == notice_id).first()
    if existing_notice:
        db.delete(existing_notice)
        db.commit()
    return existing_notice

