from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, crud, database

router = APIRouter()

# 의존성 : 데이터베이스 세션
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# 게시글 작성
@router.post("/notice/", response_model=schemas.NoticeResponse, status_code=status.HTTP_201_CREATED)
def create_notice(notice: schemas.NoticeCreate, db: Session = Depends(get_db)):
    return crud.create_notice(db=db, notice=notice)

# 게시글 목록 조회
@router.get("/notice/", response_model=list[schemas.NoticeResponse], status_code=status.HTTP_200_OK)
def read_notices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_notices(db=db, skip=skip, limit=limit)

# 특정 게시글 조회
@router.get("/notice/{notice_id}", response_model=schemas.NoticeResponse)
def read_notice(notice_id: int, db: Session = Depends(get_db)):
    notice = crud.get_notice_by_id(db=db, notice_id=notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

# 게시글 수정
@router.put("/notice/{notice_id}/edit", response_model=schemas.NoticeResponse)
def update_notice(notice_id: int, notice: schemas.NoticeUpdate, db: Session = Depends(get_db)):
    updated_notice = crud.update_notice(db=db, notice_id=notice_id, notice=notice)
    if not updated_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return updated_notice

# 게시글 삭제
@router.delete("/notice/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    delete_notice = crud.delete_notice(db=db, notice_id=notice_id)
    if not delete_notice:
        raise HTTPException(status_code=404, detail="Notice not found")