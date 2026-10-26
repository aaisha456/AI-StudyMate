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
    """
    Return progress data for the currently logged-in user.
    """

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
            SELECT
                topics_studied,
                concepts_practiced,
                flashcards_reviewed,
                understanding_percentage
            FROM student_progress
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        if not progress:

            return jsonify({
                "success": True,
                "progress": {
                    "topics_studied": 0,
                    "concepts_practiced": 0,
                    "flashcards_reviewed": 0,
                    "understanding_percentage": 0
                }
            }), 200

        return jsonify({
            "success": True,
            "progress": {
                "topics_studied": progress["topics_studied"] or 0,
                "concepts_practiced": progress["concepts_practiced"] or 0,
                "flashcards_reviewed": progress["flashcards_reviewed"] or 0,
                "understanding_percentage":
                    progress["understanding_percentage"] or 0
            }
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
    """
    Update the student's progress after completing
    a learning activity.

    Supported activity types:

    topic_studied
    concept_practiced
    flashcard_reviewed
    understanding
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

    activity_type = data.get(
        "activity_type",
        ""
    ).strip()

    topic = data.get(
        "topic",
        ""
    ).strip()

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

        # ----------------------------------------------------
        # Check whether progress already exists
        # ----------------------------------------------------

        existing_progress = connection.execute(
            """
            SELECT
                topics_studied,
                concepts_practiced,
                flashcards_reviewed,
                understanding_percentage
            FROM student_progress
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()


        # ----------------------------------------------------
        # Create initial progress record
        # ----------------------------------------------------

        if not existing_progress:

            connection.execute(
                """
                INSERT INTO student_progress (
                    user_id,
                    topics_studied,
                    concepts_practiced,
                    flashcards_reviewed,
                    understanding_percentage
                )
                VALUES (?, 0, 0, 0, 0)
                """,
                (user_id,)
            )

            connection.commit()

            existing_progress = connection.execute(
                """
                SELECT
                    topics_studied,
                    concepts_practiced,
                    flashcards_reviewed,
                    understanding_percentage
                FROM student_progress
                WHERE user_id = ?
                """,
                (user_id,)
            ).fetchone()


        # ----------------------------------------------------
        # Current values
        # ----------------------------------------------------

        topics_studied = (
            existing_progress["topics_studied"] or 0
        )

        concepts_practiced = (
            existing_progress["concepts_practiced"] or 0
        )

        flashcards_reviewed = (
            existing_progress["flashcards_reviewed"] or 0
        )

        understanding_percentage = (
            existing_progress["understanding_percentage"] or 0
        )


        # ----------------------------------------------------
        # Update activity
        # ----------------------------------------------------

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

            score = max(
                0,
                min(100, score)
            )

            # ------------------------------------------------
            # Use the latest understanding result.
            # ------------------------------------------------

            understanding_percentage = round(score)


        # ----------------------------------------------------
        # Save progress
        # ----------------------------------------------------

        connection.execute(
            """
            UPDATE student_progress
            SET
                topics_studied = ?,
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


        # ----------------------------------------------------
        # Return updated progress
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "message": "Progress updated successfully.",
            "progress": {
                "topics_studied": topics_studied,
                "concepts_practiced": concepts_practiced,
                "flashcards_reviewed": flashcards_reviewed,
                "understanding_percentage":
                    understanding_percentage
            }
        }), 200

    except Exception as error:

        connection.rollback()

        print(
            "Record activity error:",
            error
        )

        return jsonify({
            "success": False,
            "message": "Unable to update progress."
        }), 500

    finally:

        connection.close()