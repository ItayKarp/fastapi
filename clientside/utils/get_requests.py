import requests
from pydantic import RootModel, BaseModel
BASE_URL = "http://127.0.0.1:8000"
category = 'books'
FULL_PATH = f"{BASE_URL}/{category}/"


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    price: float
    is_available: bool



class DictBookModel(RootModel):
    root: dict[int, BookModel]

    def print_inventory(self):
        for key, book in self.root.items():
            print(f"""
{key}.
    Title: {book.title}
    Author: {book.author}
    Price: {book.price}$
    Availability: {book.is_available}
""")


def get_book_storage():
    response = requests.get(f'{BASE_URL}/books')
    response.raise_for_status()
    data = response.json()
    library = DictBookModel(root=data)
    library.print_inventory()
    input("Press Enter to continue...")
    return library


def get_book_info():
    book_id = input("Book id: ")
    id_path = f'{FULL_PATH}{book_id}'
    response = requests.get(
        id_path
    )
    response.raise_for_status()
    data = response.json()
    print(data)
    return data