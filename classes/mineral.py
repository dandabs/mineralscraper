import sqlite3

from helpers.sqlite import SQLiteHelper


class Mineral:
    def __init__(self, url: str, name: str, origin: str, price: str, image: str = "", description: str = ""):
        self.url = url
        self.name = name
        self.description = description
        self.origin = origin
        self.price = price
        self.image = image

    def check_unique(self):
        db = SQLiteHelper("main.db")
        query = "SELECT * FROM minerals WHERE url=?;"
        users = db.fetch_all(query, (self.url,))
        if len(users) == 0:
            return True
        else:
            return False

    def save(self):
        if self.check_unique():
            db = SQLiteHelper("main.db")
            query = "INSERT INTO minerals (url, name, description, origin, price, image) VALUES (?, ?, ?, ?, ?, ?);"
            db.execute_query(query, (self.url, self.name, self.description, self.origin, self.price, self.image))
            print(f"Saved new {self.name}")
        else:
            print(f"Did not save {self.name}, already exists")