from flask import Blueprint, request, jsonify, session

from services.ai_service import( generate_mcqs, evaluate_short_answer_local)

quiz_bp = Blueprint(
    "quiz",
    __name__,
    url_prefix="/api/quiz"
)


@quiz_bp.route("/generate", methods=["POST"])
def generate_quiz():

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


    topic = data.get(
        "topic",
        ""
    ).strip()

    study_material = data.get(
        "study_material",
        ""
    ).strip()


    if not topic:
        return jsonify({
            "success": False,
            "message": "Topic is required."
        }), 400


    if not study_material:
        return jsonify({
            "success": False,
            "message": "Study material is required."
        }), 400


    try:

        questions = generate_mcqs(
            topic,
            study_material
        )


        return jsonify({
            "success": True,
            "topic": topic,
            "questions": questions
        }), 200


    except Exception as error:

        print(
            "MCQ generation error:",
            error
        )

        return jsonify({
            "success": False,
            "message": "Unable to generate MCQs."
        }), 500


@quiz_bp.route("/short-answer", methods=["POST"])
def evaluate_short_answer():

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

    topic = data.get("topic", "").strip()
    question = data.get("question", "").strip()
    student_answer = data.get(
        "student_answer",
        ""
    ).strip()

    if not topic or not question or not student_answer:
        return jsonify({
            "success": False,
            "message": "Topic, question and answer are required."
        }), 400

    try:

        evaluation = evaluate_short_answer_local(
            topic,
            question,
            student_answer
        )

        return jsonify({
            "success": True,
            "evaluation": evaluation
        }), 200

    except Exception as error:

        print(
            "Short answer evaluation error:",
            error
        )

        return jsonify({
            "success": False,
            "message": "Unable to evaluate the answer."
        }), 500