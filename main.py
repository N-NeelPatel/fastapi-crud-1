from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from database import get_db, engine
from typing import Optional
import models
import schemas
import csv

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", status_code=status.HTTP_201_CREATED)
async def root(db: Session = Depends(get_db)):
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dic = {"name": row["name"]}
            new_author = models.Records(**dic)
            db.add(new_author)
            db.commit()
            db.refresh(new_author)

    return {"message": "authors added succesfully"}


@app.get("/authors")
async def get_authors(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    authors = db.query(models.Records).filter(
        models.Records.name.contains(search)).limit(limit).offset(skip).all()

    return authors


@app.get("/authors/{id}")
async def get_author(id: int, db: Session = Depends(get_db)):
    author = db.query(models.Records).filter(models.Records.id == id).first()

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Author with {id} not found")

    return author


@app.get("/books")
async def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()

    return books


@app.get("/books/{id}")
async def get_books(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with {id} not found")
    return book


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_info: schemas.BookData, db: Session = Depends(get_db)):
    new_book = models.Book(**book_info.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@app.put("/books/{id}")
async def update_book(id: int, book_info: schemas.BookData, db: Session = Depends(get_db)):
    book_query = db.query(models.Book).filter(models.Book.id == id)
    selected_book = book_query.first()

    if selected_book == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found the one you are looking for",
        )

    book_query.update(book_info.dict(), synchronize_session=False)
    db.commit()

    return book_query.first()


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    id: int,
    db: Session = Depends(get_db),
):
    book = db.query(models.Book).filter(models.Book.id == id)

    if book.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found the one you are looking for",
        )

    book.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
