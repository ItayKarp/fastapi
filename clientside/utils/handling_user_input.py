from typing import Callable
from .get_requests import get_book_info,get_book_storage
from .post_requests import create_book
from .put_requests import  update_book_details
from .delete_requests import delete_book, exit_menu


BASE_URL = "http://127.0.0.1:8000"
category = 'books'
FULL_PATH = f"{BASE_URL}/{category}/"

def handle_user_input(user_input):
    options: dict[str, Callable] = {
        '1':create_book,
        '2':get_book_storage,
        '3':get_book_info,
        '4':update_book_details,
        '5':delete_book,
        '6':exit_menu
    }
    action = options.get(user_input)
    if action:
        action()
    else:
        print("Invalid selection. Please choose 1-6.")


def instructions():
    print("""
Welcome to Itay's Bookshop
operations:
1. Create book
2. Book storage
3. Get book info
4. Update book details
5. Delete book from the book storage
6. Exit
    """)

def main_menu():
    while True:
        instructions()
        user_input=input("")
        handle_user_input(user_input)

if __name__ == "__main__":
    main_menu()