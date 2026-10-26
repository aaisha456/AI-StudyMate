import sqlite3
from pathlib import Path


# Get the database folder path
DATABASE_DIR = Path(__file__).resolve().parent

# Database file location
DATABASE_PATH = DATABASE_DIR / "studymate.db"

# SQL schema file location
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


def initialize_database():
    """
    Create the SQLite database and apply the database schema.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema = schema_file.read()

        connection.executescript(schema)
        connection.commit()

        print("AI StudyMate database initialized successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()