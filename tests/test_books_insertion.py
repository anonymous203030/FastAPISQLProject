import requests
import random
import string

API_URL = "http://127.0.0.1:8000/books"
NUM_BOOKS = 1000


def generate_random_string(length=random.randint(2, 100)):
    """Generate random string for book title and author test

    :param length: string length randomly from 2 to 100
    :return:
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def insert_books():
    """POST REQUEST to send data to /books

    :return:
    """
    for _ in range(NUM_BOOKS):
        book_data = {
            "title": generate_random_string(),
            "author": generate_random_string(),
        }
        response = requests.post(API_URL, json=book_data)

        if response.status_code == 200:
            print(f"Book '{book_data['title']}' added successfully.")
        else:
            print(f"Failed to add book '{book_data['title']}'.")


if __name__ == "__main__":
    insert_books()
