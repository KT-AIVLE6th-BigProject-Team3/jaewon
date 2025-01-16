from fastapi import APIRouter, Form, Depends, HTTPException, Request # HTTPException, Request 추가
from sqlalchemy.orm import Session
from sqlalchemy import desc # 목록 최신순 출력을 위한 내림차순 추가
from app.database import SessionLocal
from app.models import QnA, Notice

from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

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
    return JSONResponse(content={"message": "Question created successfully"})

# 목록 조회
@router.get("/qna/list", response_class=HTMLResponse)
def list_question(
    request: Request,
    page: int = 0, # 목록 페이지 번호
    limit: int = 10, # 페이지당 출력할 게시글 수
    db: Session = Depends(lambda: SessionLocal())
):
    qnas = db.query(QnA).order_by(desc(QnA.created_at)).offset(page * limit).limit(limit).all()
    qna_list = [
        {
            "id" : qna.id,
            "title" : qna.title,
            "created_at" : qna.created_at.isoformat(),
            "reply_title" : qna.reply_title # replied or not
        }
        for qna in qnas
    ]
    
    return templates.TemplateResponse(
        "QnA.html",
        {
            "request" : request,
            "qnaList" : qna_list
        }
    )
    
# 특정 게시글 조회
@router.get("/qna/content/{id}", response_class=HTMLResponse)
def read_question(
    request: Request,
    id: int,
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(QnA).filter(QnA.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="QnA content not found")
    
    qna_content = {
        "id" : existing.id,
        "user_id" : existing.user_id,
        "title" : existing.title,
        "content" : existing.content,
        "created_at" : existing.created_at.isoformat(),
        "reply_user" : existing.reply_user,
        "reply_title" : existing.reply_title,
        "reply_content" : existing.reply_content
    }
    return templates.TemplateResponse(
        "QnA_page.html",
        {
            "request" : request,
            "qna_content" : qna_content
        }
    )

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
@router.get("/notice/list", response_class=HTMLResponse)
def list_notice(
    request: Request,
    page: int = 0, # 목록 페이지 번호
    limit: int = 10, # 페이지당 출력할 게시글 수
    db: Session = Depends(lambda: SessionLocal())
):
    notices = db.query(Notice).order_by(desc(Notice.created_at)).offset(page * limit).limit(limit).all()
    notice_list = [
        {
            "id" : notice.id,
            "title" : notice.title,
            "created_at" : notice.created_at.isoformat()
        }
        for notice in notices
    ]
    
    return templates.TemplateResponse(
        "notice.html",
        {
            "request" : request,
            "noticeList" : notice_list
        }
    )

# 특정 게시글 조회
@router.get("/notice/content/{id}", response_class=HTMLResponse)
def read_notice(
    request: Request,
    id: int,
    db: Session = Depends(lambda: SessionLocal())
):
    existing = db.query(Notice).filter(Notice.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Notice content not found")
    
    notice_content = {
            "id" : existing.id,
            "user_id" : existing.user_id,
            "title" : existing.title,
            "content" : existing.content,
            "created_at" : existing.created_at.isoformat()
    }
    return templates.TemplateResponse(
        "notice_page.html",
        {
            "request" : request,
            "notice_content" : notice_content
        }
    )

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