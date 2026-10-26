from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from pathlib import Path

from database.db import get_db_connection
from routes.progress_routes import record_activity
from services.pdf_services import extract_text_from_pdf


study_bp = Blueprint(
    "study",
    __name__,
    url_prefix="/api/study"
)


# ============================================================
# ADD STUDY MATERIAL
# ============================================================

@study_bp.route("/materials", methods=["POST"])
def add_study_material():
    """
    Add study material for the currently logged-in student.

    Saving study material also records one studied topic
    in the student's progress.
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

    subject_name = data.get(
        "subject_name",
        ""
    ).strip()

    topic_name = data.get(
        "topic_name",
        ""
    ).strip()

    material_title = data.get(
        "material_title",
        ""
    ).strip()

    material_content = data.get(
        "material_content",
        ""
    ).strip()

    if not subject_name or not topic_name or not material_title:

        return jsonify({
            "success": False,
            "message": (
                "Subject, topic and material title "
                "are required."
            )
        }), 400

    if not material_content:

        return jsonify({
            "success": False,
            "message": "Study material content is required."
        }), 400

    connection = get_db_connection()

    try:

        # ----------------------------------------------------
        # Save study material
        # ----------------------------------------------------

        cursor = connection.execute(
            """
            INSERT INTO study_materials (
                user_id,
                subject_name,
                topic_name,
                material_title,
                material_content
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                subject_name,
                topic_name,
                material_title,
                material_content
            )
        )


        # ----------------------------------------------------
        # Check existing progress
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # Create progress record if necessary
        # ----------------------------------------------------

        if not progress:

            connection.execute(
                """
                INSERT INTO student_progress (
                    user_id,
                    topics_studied,
                    concepts_practiced,
                    flashcards_reviewed,
                    understanding_percentage
                )
                VALUES (?, 1, 0, 0, 0)
                """,
                (user_id,)
            )

        else:

            # ------------------------------------------------
            # Increase topics studied
            # ------------------------------------------------

            current_topics = (
                progress["topics_studied"] or 0
            )

            connection.execute(
                """
                UPDATE student_progress
                SET topics_studied = ?
                WHERE user_id = ?
                """,
                (
                    current_topics + 1,
                    user_id
                )
            )


        connection.commit()

        return jsonify({
            "success": True,
            "message": "Study material added successfully.",
            "material_id": cursor.lastrowid
        }), 201

    except Exception as error:

        connection.rollback()

        print(
            "Add study material error:",
            error
        )

        return jsonify({
            "success": False,
            "message": (
                "An error occurred while saving "
                "study material."
            )
        }), 500

    finally:

        connection.close()

# ============================================================
# GET STUDY MATERIALS
# ============================================================

@study_bp.route("/materials", methods=["GET"])
def get_study_materials():
    """
    Return study materials belonging to the logged-in student.
    """

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User is not logged in."
        }), 401

    connection = get_db_connection()

    try:
        materials = connection.execute(
            """
            SELECT
                material_id,
                subject_name,
                topic_name,
                material_title,
                material_content,
                created_at
            FROM study_materials
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()

        material_list = []

        for material in materials:
            material_list.append({
                "material_id": material["material_id"],
                "subject_name": material["subject_name"],
                "topic_name": material["topic_name"],
                "material_title": material["material_title"],
                "material_content": material["material_content"],
                "created_at": material["created_at"]
            })

        return jsonify({
            "success": True,
            "materials": material_list
        }), 200

    except Exception as error:
        print("Get study materials error:", error)

        return jsonify({
            "success": False,
            "message": "An error occurred while retrieving study materials."
        }), 500

    finally:
        connection.close()


# ============================================================
# UPLOAD PDF AND EXTRACT TEXT
# ============================================================

@study_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    """
    Upload a PDF, extract its readable text,
    save it as study material and return the extracted content.
    """

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    if "pdf" not in request.files:
        return jsonify({
            "success": False,
            "message": "No PDF file was uploaded."
        }), 400

    pdf_file = request.files["pdf"]

    if pdf_file.filename == "":
        return jsonify({
            "success": False,
            "message": "Please select a PDF file."
        }), 400

    original_filename = pdf_file.filename

    if not original_filename.lower().endswith(".pdf"):
        return jsonify({
            "success": False,
            "message": "Only PDF files are allowed."
        }), 400

    # Create upload directory
    base_dir = Path(__file__).resolve().parent.parent
    upload_directory = base_dir / "uploads"

    upload_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create safe filename
    safe_filename = secure_filename(original_filename)

    if not safe_filename:
        return jsonify({
            "success": False,
            "message": "Invalid PDF filename."
        }), 400

    file_path = upload_directory / safe_filename

    # Avoid duplicate filenames
    counter = 1

    while file_path.exists():
        file_path = upload_directory / (
            f"{Path(safe_filename).stem}_{counter}.pdf"
        )
        counter += 1

    try:

        # Save PDF temporarily
        pdf_file.save(file_path)

        # Extract PDF text
        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text:
            return jsonify({
                "success": False,
                "message": (
                    "The PDF was uploaded, but no readable text "
                    "could be extracted. It may be a scanned or "
                    "image-based PDF."
                )
            }), 400

        # Use filename as title
        title = Path(original_filename).stem

        subject_name = "General"
        topic_name = title
        material_title = title
        material_content = extracted_text

        # Save extracted text to database
        connection = get_db_connection()

        try:

            cursor = connection.execute(
                """
                INSERT INTO study_materials (
                    user_id,
                    subject_name,
                    topic_name,
                    material_title,
                    material_content
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    subject_name,
                    topic_name,
                    material_title,
                    material_content
                )
            )

            material_id = cursor.lastrowid

            connection.commit()

        except Exception:

            connection.rollback()
            raise

        finally:
            connection.close()

        # Return result to frontend
        return jsonify({
            "success": True,
            "message": "PDF uploaded and text extracted successfully.",
            "material_id": material_id,
            "filename": original_filename,
            "title": title,
            "subject": subject_name,
            "topic": topic_name,
            "extracted_text": extracted_text
        }), 200

    except Exception as error:

        print("PDF upload error:", error)

        return jsonify({
            "success": False,
            "message": "An error occurred while processing the PDF.",
            "error": str(error)
        }), 500

    finally:

        # Delete temporary PDF after extraction
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as cleanup_error:
            print("PDF cleanup error:", cleanup_error)