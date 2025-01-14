from fastapi import APIRouter, Form, Depends, HTTPException # HTTPException 추가
from sqlalchemy.orm import Session
from sqlalchemy import desc # 목록 최신순 출력을 위한 내림차순 추가
from app.database import SessionLocal
from app.models import QnA, Notice

router = APIRouter()

# existing = 조회 / 수정 / 삭제 함수에서 해당 id 게시글(이 존재하는지) 저장
## QnA 부분 (기존 =  post(create)만 있었음)
################ 게시글 작성
@router.post("/qna/create")
def create_question(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(lambda: SessionLocal())
):
    new_question = QnA(title=title, content=content, user_id=user_id)
    db.add(new_question)
    db.commit()
    return {"message": "Question created successfully"}

# 목록 조회
@router.get("/qna/list")
def list_question(
    page: int = 0, # 목록 페이지 번호
    limit: int = 10, # 페이지당 출력할 게시글 수
    db: Session = Depends(lambda: SessionLocal())
):
    return db.query(QnA).order_by(desc(QnA.created_at)).offset(page * limit).limit(limit).all()

# 특정 게시글 조회
@router.get("/qna/content/{id}")
def read_question(
    id: int,
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(QnA).filter(QnA.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="QnA content not found")
    return existing

# 게시글 수정
@router.put("/qna/content/{id}/edit")
def edit_question(
    id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(QnA).filter(QnA.id == id).first() # 기존 content 이름을 existing으로 하여 입력받는 게시글 내용(content)와 이름 중복 방지
    if not existing:
        raise HTTPException(status_code=404, detail="QnA content not found")
    if title:
        existing.title = title
    if content:
        existing.content = content
        
    db.commit()
    db.refresh(existing)
    
    return existing

# 게시글 답변
@router.put("/qna/content/{id}/reply")
def reply_question(
    id: int,
    reply_title: str = Form(...),
    reply_content: str = Form(...),
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(QnA).filter(QnA.id == id).first() # 기존 content 이름을 existing으로 하여 입력받는 게시글 내용(content)와 이름 중복 방지
    if not existing:
        raise HTTPException(status_code=404, detail="QnA content not found")
    existing.reply_title = reply_title
    existing.reply_content = reply_content
        
    db.commit()
    db.refresh(existing)
    
    return existing

# 게시글 삭제
@router.delete("/qna/content/{id}/delete")
def delete_qna(
    id: int,
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(QnA).filter(QnA.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="QnA not found")
    db.delete(existing)
    db.commit()
    return existing
    


##################### 공지사항(Notice)
@router.post("/notice/create")
def create_notice(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(lambda: SessionLocal())
):
    new_notice = Notice(title=title, content=content, user_id=user_id)
    db.add(new_notice)
    db.commit()
    return {"message": "New Notice created successfully"}

# 목록 조회
@router.get("/notice/list")
def list_notice(
    page: int = 0, # 목록 페이지 번호
    limit: int = 10, # 페이지당 출력할 게시글 수
    db: Session = Depends(lambda: SessionLocal())
):
    return db.query(Notice).order_by(desc(Notice.created_at)).offset(page * limit).limit(limit).all()

# 특정 게시글 조회
@router.get("/notice/content/{id}")
def read_notice(
    id: int,
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(Notice).filter(Notice.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Notice content not found")
    return existing

# 게시글 수정
@router.put("/notice/content/{id}/edit")
def edit_notice(
    id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(Notice).filter(Notice.id == id).first() # 기존 content 이름을 existing으로 하여 입력받는 게시글 내용(content)와 이름 중복 방지
    if not existing:
        raise HTTPException(status_code=404, detail="Notice content not found")
    if title:
        existing.title = title
    if content:
        existing.content = content
        
    db.commit()
    db.refresh(existing)
    
    return existing

# 게시글 삭제
@router.delete("/notice/content/{id}/delete")
def delete_notice(
    id: int,
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(Notice).filter(Notice.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Notice not found")
    db.delete(existing)
    db.commit()
    return existing