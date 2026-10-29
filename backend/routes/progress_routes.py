from flask import Blueprint, request, jsonify, session
from database.db import get_db_connection

progress_bp = Blueprint(
    "progress",
    __name__,
    url_prefix="/api/progress"
)


# ============================================================
# GET PROGRESS
# ============================================================

@progress_bp.route("", methods=["GET"])
def get_progress():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User is not logged in."
        }), 401

    connection = get_db_connection()

    try:
        progress = connection.execute(
            """
            SELECT topics_studied, concepts_practiced,
                   flashcards_reviewed, understanding_percentage
            FROM student_progress
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        revision_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM revision_topics
            WHERE user_id = ? AND needs_revision = 1
            """,
            (user_id,)
        ).fetchone()[0]

        if not progress:
            progress_data = {
                "topics_studied": 0,
                "concepts_practiced": 0,
                "flashcards_reviewed": 0,
                "understanding_percentage": 0
            }
        else:
            progress_data = {
                "topics_studied": progress["topics_studied"] or 0,
                "concepts_practiced": progress["concepts_practiced"] or 0,
                "flashcards_reviewed": progress["flashcards_reviewed"] or 0,
                "understanding_percentage":
                    progress["understanding_percentage"] or 0
            }

        progress_data["revision_topic_count"] = revision_count

        return jsonify({
            "success": True,
            "progress": progress_data
        }), 200

    except Exception as error:
        print("Get progress error:", error)
        return jsonify({
            "success": False,
            "message": "An error occurred while retrieving progress."
        }), 500

    finally:
        connection.close()


# ============================================================
# RECORD ACTIVITY
# ============================================================

@progress_bp.route("/activity", methods=["POST"])
def record_activity():
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

    activity_type = data.get("activity_type", "").strip()
    topic = data.get("topic", "").strip()
    score = data.get("score")

    if not activity_type:
        return jsonify({
            "success": False,
            "message": "Activity type is required."
        }), 400

    valid_activity_types = {
        "topic_studied",
        "concept_practiced",
        "flashcard_reviewed",
        "understanding"
    }

    if activity_type not in valid_activity_types:
        return jsonify({
            "success": False,
            "message": "Invalid activity type."
        }), 400

    connection = get_db_connection()

    try:
        existing_progress = connection.execute(
            """
            SELECT topics_studied, concepts_practiced,
                   flashcards_reviewed, understanding_percentage
            FROM student_progress
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        if not existing_progress:
            connection.execute(
                """
                INSERT INTO student_progress (
                    user_id, topics_studied, concepts_practiced,
                    flashcards_reviewed, understanding_percentage
                )
                VALUES (?, 0, 0, 0, 0)
                """,
                (user_id,)
            )

            existing_progress = connection.execute(
                """
                SELECT topics_studied, concepts_practiced,
                       flashcards_reviewed, understanding_percentage
                FROM student_progress
                WHERE user_id = ?
                """,
                (user_id,)
            ).fetchone()

        topics_studied = existing_progress["topics_studied"] or 0
        concepts_practiced = existing_progress["concepts_practiced"] or 0
        flashcards_reviewed = existing_progress["flashcards_reviewed"] or 0
        understanding_percentage = (
            existing_progress["understanding_percentage"] or 0
        )

        if activity_type == "topic_studied":
            topics_studied += 1

        elif activity_type == "concept_practiced":
            concepts_practiced += 1

        elif activity_type == "flashcard_reviewed":
            flashcards_reviewed += 1

        elif activity_type == "understanding":
            if score is None:
                return jsonify({
                    "success": False,
                    "message": "Understanding score is required."
                }), 400

            try:
                score = float(score)
            except (TypeError, ValueError):
                return jsonify({
                    "success": False,
                    "message": "Understanding score must be numeric."
                }), 400

            score = max(0, min(100, score))

            # Save or update the topic for Smart Revision
            if topic:
                connection.execute(
                    """
                    INSERT INTO revision_topics (
                        user_id, topic_name, understanding_percentage,
                        needs_revision, updated_at
                    )
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(user_id, topic_name)
                    DO UPDATE SET
                        understanding_percentage = excluded.understanding_percentage,
                        needs_revision = excluded.needs_revision,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        user_id,
                        topic,
                        score,
                        1 if score < 80 else 0
                    )
                )

            understanding_percentage = round(score)

        connection.execute(
            """
            UPDATE student_progress
            SET topics_studied = ?,
                concepts_practiced = ?,
                flashcards_reviewed = ?,
                understanding_percentage = ?
            WHERE user_id = ?
            """,
            (
                topics_studied,
                concepts_practiced,
                flashcards_reviewed,
                understanding_percentage,
                user_id
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Progress updated successfully.",
            "progress": {
                "topics_studied": topics_studied,
                "concepts_practiced": concepts_practiced,
                "flashcards_reviewed": flashcards_reviewed,
                "understanding_percentage": understanding_percentage
            }
        }), 200

    except Exception as error:
        connection.rollback()
        print("Record activity error:", error)
        return jsonify({
            "success": False,
            "message": "Unable to update progress."
        }), 500

    finally:
        connection.close()