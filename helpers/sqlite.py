import sqlite3
from typing import List, Tuple, Any, Optional

class SQLiteHelper:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()

    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple[Any]]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Tuple[Any]]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchone()