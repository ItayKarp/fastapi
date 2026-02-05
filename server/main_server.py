from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(docs_url="/administrator123")
BOOKS_PATH = './books'
os.makedirs(BOOKS_PATH, exist_ok=True)

class BookModel(BaseModel):
    title : str
    author : str
    price : float | int

class BookUpdateModel(BaseModel):
    title : str = ""
    author : str = ""
    price : float | int = 0

class Book:
    _id_counter = 0
    def __init__(self, title, author, price,  is_available = True, book_id = None):
        if book_id:
            self.id = book_id
            if book_id > self.id:
                Book._id_counter = book_id
        else:
            Book._id_counter += 1
            self.id = Book._id_counter
        self.title = title
        self.author = author
        self.price = price
        self.is_available = is_available

    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title

Books: dict[int, Book | BookModel] = {}

def initialize_library():
    for book_id in os.listdir(BOOKS_PATH):
        if book_id.endswith(".txt"):
            book_data = {}
            book_path = os.path.join(BOOKS_PATH, book_id)
            with open(book_path, "r", encoding="utf-8") as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        book_data[key.strip()] = value.strip()
            if book_data:
                old_book_id = int(book_data['ID'])
                old_book_title = book_data['Title']
                old_book_author = book_data['Author']
                old_book_price = float(book_data['Price'])
                old_book_title = Book(old_book_title, old_book_author, old_book_price, book_id=old_book_id)
                Books[old_book_id] = old_book_title

initialize_library()

@app.get("/books/{book_id}")
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

@app.get("/books")
async def get_books():
    return Books

@app.post("/books/")
async def create_book(book_in: BookModel, type: str = None):
    if type == "create":
        new_book = Book(book_in.title, book_in.author, book_in.price)
        Books[new_book.id] = new_book
        create_file(new_book)
    else:
        raise HTTPException(status_code=404, detail="Path not found.")

@app.put("/books/")
async def update_details(book_id: int, new_book: BookModel, type: str = None):
    if type == "update_details":
        if book_id not in Books:
            raise HTTPException(status_code=404, detail="Book not found")
        book = Book(new_book.title, new_book.author, new_book.price, book_id=book_id)
        create_file(book)
        return {'status': 'Success', 'new details': new_book}
    else:
        raise HTTPException(status_code=404, detail="Path not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    delete_path = os.path.join(BOOKS_PATH, f'book_{book_id}.txt')
    if os.path.exists(delete_path):
        os.remove(delete_path)
        del Books[book_id]
        return {'status': 'Success', 'id': book_id}
    else:
        raise HTTPException(status_code=404, detail="Book not found")


def create_file(book: Book | BookModel):
    book_path = os.path.join(BOOKS_PATH, f'book_{book.id}.txt')
    content = [
        f"ID:{book.id}",
        f"Title:{book.title}",
        f"Author:{book.author}",
        f"Price:{book.price}",
        f"Is_Available:{book.is_available}"
    ]
    with open(book_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(content))