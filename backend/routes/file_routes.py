from flask import Blueprint, request, jsonify, session
from pathlib import Path
from werkzeug.utils import secure_filename

from services.file_service import extract_text_from_file


file_bp = Blueprint("file", __name__, url_prefix="/api/files")


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def allowed_file(filename):
    """Check whether the uploaded file has an allowed extension."""

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


@file_bp.route("/upload", methods=["POST"])
def upload_file():

    # Make sure the student is logged in.
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User is not logged in."
        }), 401

    # Check whether a file was submitted.
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file was uploaded."
        }), 400

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return jsonify({
            "success": False,
            "message": "Please select a file."
        }), 400

    # Check file type.
    if not allowed_file(uploaded_file.filename):
        return jsonify({
            "success": False,
            "message": "Only PDF, DOCX, and TXT files are supported."
        }), 400

    # Create the uploads folder if it does not exist.
    UPLOAD_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create a safe filename.
    filename = secure_filename(
        uploaded_file.filename
    )

    # Add user ID to avoid filename conflicts.
    filename = f"user_{user_id}_{filename}"

    file_path = UPLOAD_FOLDER / filename

    # Save the uploaded file.
    uploaded_file.save(file_path)

    try:

        # Extract text from the uploaded file.
        extracted_text = extract_text_from_file(
            file_path
        )

        if not extracted_text:
            return jsonify({
                "success": False,
                "message": (
                    "The file was uploaded, "
                    "but no readable text was found."
                )
            }), 400

        return jsonify({
            "success": True,
            "message": "File uploaded successfully.",
            "filename": filename,
            "text": extracted_text
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": (
                "Unable to extract text from the file."
            ),
            "error": str(error)
        }), 500