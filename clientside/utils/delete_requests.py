import requests
from .get_requests import FULL_PATH



def delete_book():
    book_id = input("Book id: ")
    id_path = f'{FULL_PATH}{book_id}'
    response = requests.delete(
        id_path
    )
    response.raise_for_status()
    data = response.json()
    print(data)
    return data

def exit_menu():
    sys.exit()
