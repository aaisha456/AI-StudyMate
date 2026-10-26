from flask import Blueprint, request, jsonify, session

from database.db import get_db_connection


flashcard_bp = Blueprint(
    "flashcard",
    __name__,
    url_prefix="/api/flashcards"
)


@flashcard_bp.route("", methods=["POST"])
def create_flashcard():
    """
    Save a flashcard for the logged-in student.
    """

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User is not logged in."
        }), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request data is required."
        }), 400

    topic_name = data.get("topic_name", "").strip()
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()

    if not topic_name:
        return jsonify({
            "success": False,
            "message": "Topic name is required."
        }), 400

    if not question:
        return jsonify({
            "success": False,
            "message": "Flashcard question is required."
        }), 400

    if not answer:
        return jsonify({
            "success": False,
            "message": "Flashcard answer is required."
        }), 400

    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO flashcards (
                user_id,
                topic_name,
                question,
                answer
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                topic_name,
                question,
                answer
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Flashcard saved successfully.",
            "flashcard_id": cursor.lastrowid
        }), 201

    except Exception:
        connection.rollback()

        return jsonify({
            "success": False,
            "message": "An error occurred while saving the flashcard."
        }), 500

    finally:
        connection.close()


@flashcard_bp.route("", methods=["GET"])
def get_flashcards():
    """
    Retrieve flashcards belonging to the logged-in student.
    """

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User is not logged in."
        }), 401

    topic_name = request.args.get(
        "topic",
        ""
    ).strip()

    connection = get_db_connection()

    try:
        if topic_name:
            flashcards = connection.execute(
                """
                SELECT
                    flashcard_id,
                    topic_name,
                    question,
                    answer,
                    created_at
                FROM flashcards
                WHERE user_id = ?
                AND topic_name = ?
                ORDER BY created_at ASC
                """,
                (
                    user_id,
                    topic_name
                )
            ).fetchall()

        else:
            flashcards = connection.execute(
                """
                SELECT
                    flashcard_id,
                    topic_name,
                    question,
                    answer,
                    created_at
                FROM flashcards
                WHERE user_id = ?
                ORDER BY created_at ASC
                """,
                (user_id,)
            ).fetchall()

        flashcard_list = []

        for flashcard in flashcards:
            flashcard_list.append({
                "flashcard_id": flashcard["flashcard_id"],
                "topic_name": flashcard["topic_name"],
                "question": flashcard["question"],
                "answer": flashcard["answer"],
                "created_at": flashcard["created_at"]
            })

        return jsonify({
            "success": True,
            "flashcards": flashcard_list
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "An error occurred while retrieving flashcards."
        }), 500

    finally:
        connection.close()