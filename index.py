# sbeeve harvey

import os
import importlib.util

from helpers.sqlite import SQLiteHelper

from menu import (
    search_by_name,
    list_by_origin,
    show_top_10_cheapest,
    show_top_10_expensive,
)


def init_database():
    db = SQLiteHelper("main.db")
    query = """
    CREATE TABLE IF NOT EXISTS minerals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        origin TEXT NOT NULL,
        price TEXT NOT NULL,
        image TEXT NOT NULL
    );
    """
    db.execute_query(query)
    print("Initialized database")

def run_scrapers_sync(directory='sites'):
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    for file_name in os.listdir(directory):
        if file_name.endswith(".py"):
            file_path = os.path.join(directory, file_name)

            spec = importlib.util.spec_from_file_location(file_name[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)

                if hasattr(module, "main") and callable(module.main):
                    print(f"Running 'main()' from {file_name}")
                    module.main()
                else:
                    print(f"No 'main' function found in {file_name}")
            except Exception as e:
                print(f"Error running {file_name}: {e}")

init_database()

def main():
    db = SQLiteHelper("main.db")

    while True:
        print("\nMineral Scraper Menu:")
        print("0. Run scraper")
        print("1. Search for a mineral by name")
        print("2. List minerals by origin location")
        print("3. Show top 10 cheapest minerals")
        print("4. Show top 10 most expensive minerals")
        print("5. Exit")

        choice = input("Enter your choice (0-5): ").strip()

        if choice == "0":
            run_scrapers_sync()
        if choice == "1":
            search_by_name(db)
        elif choice == "2":
            list_by_origin(db)
        elif choice == "3":
            show_top_10_cheapest(db)
        elif choice == "4":
            show_top_10_expensive(db)
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()