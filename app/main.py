# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base
#from app.schemas import 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


def commit_or_rollback(db.Session, error_msg:str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    raise HTTPException(status_code=409, detail=error_msg)

# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/authors",response_model = AuthorRead, status_code=201)
def create_author(db:Session = Depends(get_db)):
    db_author = AuthorDB(**Author.model.dump())
    db.add(db_author)
    commit_or_rollback(db, "Author Already Exists")
    db.refresh(db_author)
    return db_author

@app.get("/api/authors",response_model = AuthorRead)
    def list_authors(db:Session = Depends(get_db)):
        stmt = select(AuthorDB).order_by(AuthorDB.id)
        
        result = db.execute(stmt)
        authors = result.scalars().all()
        return authors
    
@app.get("/api/authors/{id}", response_model = AuthorRead)
    def get_authors(id: int, Session = Depends(get_db)):
        Author = db.get(AuthorDB, id)
        if not Author:
            raise HTTPException(status_code = 404, detail = "Author not found")
        return author

@app.patch("/api/authors/{id}", response_model = AuthorRead)
    def partial_update_author(id: int, payload: AuthorPatch, db: Session = Depends(get_db)):
        Author = db.get(AuthorDB,id)
        if not Author:
            raise HTTPException(status_code = 404, detail = "Author not Found")
        
        update_data = payload.model.dump(exclude_unset = True)
        for Field, value in update_data.items():
            setattr(Author, Field, value)
        
        commit_or_rollback(db,"Author Update Failed")
        db.refresh
        return Author

@app.delete("/api/users/{id}", status_code = 204)
def delete_Author(id = int, db:Session = Depends(get_db))->Response:
    Author=db.get(AuthorDB,id)
    if not Author:
        raise HTTPException(status_code = 404, detail = "Author not found")
    db.delete(Author)
    db.commit()
    return Repsonse(status_code=status.HTTP.204_NO_CONTENT)


#----------------------------------------------------------BOOKS-------------------------------------------------------------------------

@app.post("/api/books",response_model = BookRead, status_code = 201)
    def create_book(books: BookCreate, db:Session = Depends(get_db)):
        Author = db.get(AuthorDB,books,authors_id
        if not Author:
            raise HTTPException(status_code = 404, detail = "Author not Found") 
    books = BookDB(
        title = books.title
        pages = books.pages
        authors_id = books.authors_id
    )
    db.add(books)
    return(books)

@app.get("/api/books",response_model = BookRead)
    def list_books(db:Session = Depends(get_db)):
        stmt = select(BookDB).order_by(BookDB.id)
        
        result = db.execute(stmt)
        authors = result.scalars().all()
        return books

@app.get("/api/books/{id}", response_model = BookRead)
    def get_book(id: int, Session = Depends(get_db)):
        Books = db.get(BookDB, id)
        if not Books:
            raise HTTPException(status_code = 404, detail = "Book not found")
        return Books