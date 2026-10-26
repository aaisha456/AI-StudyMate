from flask import Blueprint, request, jsonify, session

from services.ai_service import (
    analyze_teach_back,
    generate_flashcards
)


ai_bp = Blueprint(
    "ai",
    __name__,
    url_prefix="/api/ai"
)


# ============================================================
# LOCAL AI EXPLANATION ENGINE
# ============================================================

def generate_local_explanation(topic, study_material):
    """
    Generates a structured explanation locally from the
    study material provided by the student.

    This works without an external AI API.
    """

    topic = topic.strip()
    study_material = study_material.strip()

    if not study_material:
        return "No study material was provided."

    # --------------------------------------------------------
    # Clean the material
    # --------------------------------------------------------

    text = " ".join(
        line.strip()
        for line in study_material.splitlines()
        if line.strip()
    )

    # --------------------------------------------------------
    # Split material into sentences
    # --------------------------------------------------------

    sentences = [
        sentence.strip()
        for sentence in text.replace("?", ".").replace("!", ".").split(".")
        if sentence.strip()
    ]

    # Keep explanation manageable
    important_sentences = sentences[:8]

    # --------------------------------------------------------
    # Identify important concepts
    # --------------------------------------------------------

    words = text.split()

    stop_words = {
        "this", "that", "with", "from", "which",
        "their", "there", "these", "those",
        "about", "into", "also", "have", "has",
        "been", "being", "were", "where",
        "when", "what", "will", "would",
        "could", "should", "than", "then",
        "they", "them", "such", "only",
        "more", "some", "very", "each",
        "using", "used", "uses", "does",
        "and", "the", "for", "are", "was",
        "is", "in", "of", "to", "a", "an",
        "on", "by", "as", "or", "it"
    }

    important_words = []

    for word in words:

        clean_word = (
            word.strip(".,!?;:()[]{}\"'")
            .lower()
        )

        if (
            len(clean_word) >= 5
            and clean_word not in stop_words
            and clean_word.isalpha()
        ):
            if clean_word not in important_words:
                important_words.append(clean_word)

    concepts = important_words[:8]

    # --------------------------------------------------------
    # Build explanation
    # --------------------------------------------------------

    explanation_parts = []

    explanation_parts.append(
        f"Understanding {topic}"
    )

    explanation_parts.append(
        "\n\n1. What is it?\n"
    )

    if important_sentences:

        explanation_parts.append(
            "The study material explains the topic using "
            "the following key ideas:"
        )

        for sentence in important_sentences[:3]:

            explanation_parts.append(
                f"\n• {sentence}"
            )

    else:

        explanation_parts.append(
            f"The provided material discusses {topic}."
        )

    # --------------------------------------------------------
    # Key concepts
    # --------------------------------------------------------

    explanation_parts.append(
        "\n\n2. Key concepts\n"
    )

    if concepts:

        explanation_parts.append(
            "Important concepts identified from your material:"
        )

        for concept in concepts[:6]:

            explanation_parts.append(
                f"\n• {concept.capitalize()}"
            )

    else:

        explanation_parts.append(
            "No separate key concepts could be identified."
        )

    # --------------------------------------------------------
    # Simple explanation
    # --------------------------------------------------------

    explanation_parts.append(
        "\n\n3. Simple explanation\n"
    )

    if len(important_sentences) >= 4:

        explanation_parts.append(
            "In simple terms, the topic can be understood "
            "by connecting the main ideas from the material:"
        )

        for sentence in important_sentences[3:6]:

            explanation_parts.append(
                f"\n• {sentence}"
            )

    else:

        explanation_parts.append(
            "Read the main statements above and connect "
            "them with the key concepts listed."
        )

    # --------------------------------------------------------
    # Example / application
    # --------------------------------------------------------

    explanation_parts.append(
        "\n\n4. Important points to remember\n"
    )

    if important_sentences:

        for sentence in important_sentences[-3:]:

            explanation_parts.append(
                f"\n• {sentence}"
            )

    else:

        explanation_parts.append(
            f"Focus on the definition, concepts and "
            f"applications of {topic}."
        )

    # --------------------------------------------------------
    # Revision tip
    # --------------------------------------------------------

    explanation_parts.append(
        "\n\n5. Revision tip\n"
    )

    explanation_parts.append(
        f"After studying {topic}, try explaining it in "
        "your own words using the Teach Me Back feature. "
        "This helps check whether you actually understand "
        "the concept rather than only remembering the text."
    )

    return "".join(explanation_parts)


# ============================================================
# AI EXPLANATION
# ============================================================

@ai_bp.route("/explain", methods=["POST"])
def explain_topic():

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

        # ----------------------------------------------------
        # Generate explanation locally.
        # No external API or OpenAI credits are required.
        # ----------------------------------------------------

        explanation = generate_local_explanation(
            topic,
            study_material
        )

        return jsonify({
            "success": True,
            "topic": topic,
            "explanation": explanation
        }), 200

    except Exception as error:

        print(
            "AI explanation error:",
            error
        )

        return jsonify({
            "success": False,
            "message": "Unable to generate AI explanation."
        }), 500


# ============================================================
# FLASHCARDS
# ============================================================

@ai_bp.route("/flashcards/generate", methods=["POST"])
def generate_flashcards_route():

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

        flashcards = generate_flashcards(
            topic,
            study_material
        )

        return jsonify({
            "success": True,
            "topic": topic,
            "flashcards": flashcards
        }), 200

    except Exception as error:

        print(
            "Flashcard generation error:",
            error
        )

        return jsonify({
            "success": False,
            "message": "Unable to generate flashcards."
        }), 500


# ============================================================
# TEACH ME BACK
# ============================================================

@ai_bp.route("/teach-back", methods=["POST"])
def teach_back_route():

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

    student_explanation = data.get(
        "student_explanation",
        ""
    ).strip()

    if not topic:

        return jsonify({
            "success": False,
            "message": "Topic is required."
        }), 400

    if not student_explanation:

        return jsonify({
            "success": False,
            "message": "Student explanation is required."
        }), 400

    try:

        analysis = analyze_teach_back(
            topic,
            student_explanation
        )

        return jsonify({
            "success": True,
            "topic": topic,
            "analysis": analysis
        }), 200

    except Exception as error:

        print(
            "Teach Me Back error:",
            error
        )

        return jsonify({
            "success": False,
            "message": "Unable to analyze your explanation."
        }), 500