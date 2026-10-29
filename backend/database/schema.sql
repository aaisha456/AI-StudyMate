-- =========================================
-- AI StudyMate Database Schema
-- =========================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- =========================================
-- STUDENT PROGRESS
-- =========================================

CREATE TABLE IF NOT EXISTS student_progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    topics_studied INTEGER DEFAULT 0,
    concepts_practiced INTEGER DEFAULT 0,
    flashcards_reviewed INTEGER DEFAULT 0,
    understanding_percentage REAL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================================
-- STUDY MATERIALS
-- =========================================

CREATE TABLE IF NOT EXISTS study_materials (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject_name TEXT NOT NULL,
    topic_name TEXT NOT NULL,
    material_title TEXT NOT NULL,
    material_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- =========================================
-- FLASHCARDS
-- =========================================

CREATE TABLE IF NOT EXISTS flashcards (
    flashcard_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_name TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================================
-- SMART REVISION TOPICS
-- =========================================

CREATE TABLE IF NOT EXISTS revision_topics (
    revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_name TEXT NOT NULL,
    understanding_percentage REAL NOT NULL DEFAULT 0,
    needs_revision INTEGER NOT NULL DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE (user_id, topic_name)
);