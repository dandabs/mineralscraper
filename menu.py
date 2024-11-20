import re
from helpers.sqlite import SQLiteHelper


def parse_price(price: str) -> float:
    """
    Parse a price string to extract the numeric value.
    Removes any non-numeric characters except for the decimal point.
    """
    try:
        return float(re.sub(r"[^\d.]", "", price))
    except ValueError:
        return float("inf")  # Treat invalid prices as very high


def search_by_name(db: SQLiteHelper):
    """
    Search for a mineral by name.
    """
    name = input("Enter the mineral name to search: ").strip()
    results = db.fetch_all("SELECT * FROM minerals WHERE name LIKE ?", (f"%{name}%",))
    if results:
        for row in results:
            print(f"Name: {row[2]}, Origin: {row[4]}, Price: {row[5]}, URL: {row[1]}")
    else:
        print("No minerals found with that name.")


def list_by_origin(db: SQLiteHelper):
    """
    List minerals grouped by their origin, along with the quantity in each group.
    """
    results = db.fetch_all("SELECT origin, COUNT(*) FROM minerals GROUP BY origin")
    if results:
        print("\nMinerals by origin:")
        for row in results:
            print(f"Origin: {row[0]} - Quantity: {row[1]}")
    else:
        print("No minerals found.")


def show_top_10_cheapest(db: SQLiteHelper):
    """
    Show the top 10 cheapest minerals based on alphabetical order of price.
    """
    results = db.fetch_all("SELECT * FROM minerals ORDER BY price ASC LIMIT 10")
    if results:
        print("\nTop 10 Cheapest Minerals (Alphabetical Price):")
        for row in results:
            print(f"Name: {row[2]}, Origin: {row[4]}, Price: {row[5]}, URL: {row[1]}")
    else:
        print("No minerals found.")


def show_top_10_expensive(db: SQLiteHelper):
    """
    Show the top 10 most expensive minerals based on alphabetical order of price.
    """
    results = db.fetch_all("SELECT * FROM minerals ORDER BY price DESC LIMIT 10")
    if results:
        print("\nTop 10 Most Expensive Minerals (Alphabetical Price):")
        for row in results:
            print(f"Name: {row[2]}, Origin: {row[4]}, Price: {row[5]}, URL: {row[1]}")
    else:
        print("No minerals found.")