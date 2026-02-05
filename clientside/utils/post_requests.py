from .get_requests import FULL_PATH
import requests

def create_book():
    book_data: dict[str, str] = {
        "title": input("Book title: "),
        "author": input("Author: "),
        "price": float(input("Price(must be a number): "))
    }
    parameters = {'type':'create'}
    response = requests.post(
        FULL_PATH,
        json=book_data,
        params=parameters
    )
    response.raise_for_status()
    data = response.json()
    return data