import requests
from .get_requests import FULL_PATH


def update_book_details():
    parameters = {
        'type':'update_details',
        'book_id':int(input("Book id(must be an integer): "))
    }
    book_data: dict[str, str | float] = {
        'title':input("Book title: "),
        'author':input("Author: "),
        'price':input("Book price: ")
    }
    response = requests.put(
        FULL_PATH,
        json=book_data,
        params=parameters
    )
    response.raise_for_status()
    data = response.json()
    print(data)
    return data