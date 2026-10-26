import sqlite3
from pathlib import Path


# Get the backend folder path
BASE_DIR = Path(__file__).resolve().parent.parent

# Store the SQLite database inside the database folder
DATABASE_PATH = BASE_DIR / "database" / "studymate.db"


def get_db_connection():
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Allows us to access columns by their names
    connection.row_factory = sqlite3.Row

    return connection