from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import get_db_connection


# Create an authentication Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new AI StudyMate user.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request data is required."
        }), 400

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not full_name or not email or not password:
        return jsonify({
            "success": False,
            "message": "Full name, email and password are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 8 characters."
        }), 400

    connection = get_db_connection()

    try:
        existing_user = connection.execute(
            "SELECT user_id FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:
            return jsonify({
                "success": False,
                "message": "An account with this email already exists."
            }), 409

        password_hash = generate_password_hash(password)

        connection.execute(
            """
            INSERT INTO users (full_name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (full_name, email, password_hash)
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Account created successfully."
        }), 201

    except Exception:
        connection.rollback()

        return jsonify({
            "success": False,
            "message": "An error occurred while creating the account."
        }), 500

    finally:
        connection.close()


@auth_bp.route("/login", methods=["POST"])
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate an existing AI StudyMate user.
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request data is required."
        }), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    connection = get_db_connection()

    try:
        user = connection.execute(
            """
            SELECT user_id, full_name, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if not user or not check_password_hash(
            user["password_hash"],
            password
        ):
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        session["user_id"] = user["user_id"]
        session["full_name"] = user["full_name"]
        session["email"] = user["email"]

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "user": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"]
            }
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "An error occurred while logging in."
        }), 500

    finally:
        connection.close()

@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    """
    Return the details of the currently logged-in user.
    """

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User is not logged in."
        }), 401

    connection = get_db_connection()

    try:
        user = connection.execute(
            """
            SELECT user_id, full_name, email
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        if not user:
            session.clear()

            return jsonify({
                "success": False,
                "message": "User account not found."
            }), 404

        return jsonify({
            "success": True,
            "user": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"]
            }
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "An error occurred while retrieving user details."
        }), 500

    finally:
        connection.close()