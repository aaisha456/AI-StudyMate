from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from routes.auth_routes import auth_bp
from routes.progress_routes import progress_bp
from routes.study_routes import study_bp
from routes.ai_routes import ai_bp
from routes.flashcard_routes import flashcard_bp
from routes.file_routes import file_bp
from routes.quiz_routes import quiz_bp

load_dotenv()
app = Flask(__name__)
app.secret_key="change-this-later"
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501"
]
        }
    },
    supports_credentials=True
)


# Register application routes
app.register_blueprint(auth_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(study_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(flashcard_bp)
app.register_blueprint(file_bp)
app.register_blueprint(quiz_bp)


@app.route("/")
def home():
    return jsonify({
        "message": "AI StudyMate backend is running successfully."
    })


if __name__ == "__main__":
    app.run(debug=True)