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
        
# QnA 게시글 작성
@router.post("/qna/", response_model=schemas.QnaResponse, status_code=status.HTTP_201_CREATED)
def create_qna(qna: schemas.QnaCreate, db: Session = Depends(get_db)):
    return crud.create_qna(db=db, qna=qna)

# QnA 게시글 목록 조회
@router.get("/qna/", response_model=list[schemas.QnaResponse], status_code=status.HTTP_200_OK)
def read_qna(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_qna(db=db, skip=skip, limit=limit)

# 특정 QnA 게시글 조회
@router.get("/qna/{qna_id}", response_model=schemas.QnaResponse)
def read_qna(qna_id: int, db: Session = Depends(get_db)):
    qna = crud.get_qna_by_id(db=db, qna_id=qna_id)
    if not qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    return qna

# QnA 게시글 수정 (작성자)
@router.put("/qna/{qna_id}/edit", response_model=schemas.QnaResponse)
def update_qna(qna_id: int, qna: schemas.QnaUpdate, db: Session = Depends(get_db)):
    updated_qna = crud.update_qna(db=db, qna_id=qna_id, qna=qna)
    if not updated_qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    return updated_qna

# QnA 게시글 답변 (관리자)
@router.put("/qna/{qna_id}/answer", response_model=schemas.QnaAnswer)
def answer_qna(qna_id: int, qna: schemas.QnaAnswer, db: Session = Depends(get_db)):
    answer_qna = crud.answer_qna(db=db, qna_id=qna_id, qna=qna)
    if not answer_qna:
        raise HTTPException(status_code=404, detail="QnA not found")
    return answer_qna

# 게시글 삭제
@router.delete("/qna/{qna_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_qna(qna_id: int, db: Session = Depends(get_db)):
    delete_qna = crud.delete_qna(db=db, qna_id=qna_id)
    if not delete_qna:
        raise HTTPException(status_code=404, detail="QnA not found")