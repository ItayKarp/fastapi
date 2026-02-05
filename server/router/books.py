from fastapi import FastAPI, HTTPException, APIRouter
from ..models import BookModel
from ..database import Books, Book, create_file, BOOKS_PATH, delete_book
import os

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.get("/{book_id}")
async def get_book(book_id: int):
    book_path = f'{BOOKS_PATH}/book_{book_id}.txt'
    book_data = {}
    if not os.path.exists(book_path):
        raise HTTPException(status_code=404, detail="Book not found")
    with open(book_path, "r", encoding="utf-8") as f:
        for line in f:
            if ':' in line:
                key, value = line.split(':', 1)
                book_data[key.strip().lower()] = value.strip()
    return book_data

@router.post("/")
async def create_book(book_in: BookModel, type: str = None):
    if type == "create":
        new_book = Book(book_in.title, book_in.author, book_in.price)
        Books[new_book.id] = new_book
        create_file(new_book)
    else:
        raise HTTPException(status_code=404, detail="Path not found.")

@router.put("/")
async def update_details(book_id: int, new_book: BookModel, type: str = None):
    if type == "update_details":
        if book_id not in Books:
            raise HTTPException(status_code=404, detail="Book not found")
        book = Book(new_book.title, new_book.author, new_book.price, book_id=book_id)
        create_file(book)
        return {'status': 'Success', 'new details': new_book}
    else:
        raise HTTPException(status_code=404, detail="Path not found")


@router.delete("/{book_id}")
async def delete_book_data(book_id: int):
    success = delete_book(book_id)

    if success:
        return {'status': 'Success', 'id': book_id}
    else:
        raise HTTPException(status_code=404, detail="Book not found")