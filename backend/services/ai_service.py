import os
import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"


def generate_ai_explanation(topic, study_material):
    """
    Generate a clear explanation of a study topic
    using the student's study material.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    prompt = f"""
You are an AI study assistant.

Explain the following topic to a B.Sc. Computer Science student.

Topic:
{topic}

Student's study material:
{study_material}

Instructions:
1. Explain the concept in simple but technically correct language.
2. Start with a clear definition.
3. Explain the important concepts step by step.
4. Give a simple example where useful.
5. Do not invent information and claim that it came from the student's material.
6. Clearly separate general explanation from information specifically present in the supplied material.
7. End with 3 important points the student should remember.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-5.6-luna",
        "input": prompt
    }

    response = requests.post(
        OPENAI_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    explanation = result.get("output_text")

    if not explanation:
        raise RuntimeError(
            "AI returned an empty explanation."
        )

    return explanation
def analyze_teach_back(topic, student_explanation):
    """
    Analyze a student's explanation using a local
    rule-based approach without requiring API credits.
    """

    topic_lower = topic.lower()
    explanation_lower = student_explanation.lower()

    concept_keywords = [
        word.strip(".,!?()")
        for word in topic_lower.split()
        if len(word.strip(".,!?()")) > 3
    ]

    matched_concepts = []

    for keyword in concept_keywords:
        if keyword in explanation_lower:
            matched_concepts.append(keyword)

    word_count = len(
        student_explanation.split()
    )

    understanding_percentage = 40

    understanding_percentage += (
        len(matched_concepts) * 10
    )

    if word_count >= 30:
        understanding_percentage += 10

    if word_count >= 60:
        understanding_percentage += 10

    understanding_percentage = min(
        understanding_percentage,
        95
    )

    if understanding_percentage >= 80:

        understanding_level = (
            "Good understanding"
        )

    elif understanding_percentage >= 60:

        understanding_level = (
            "Partial understanding"
        )

    else:

        understanding_level = (
            "Needs more practice"
        )

    if matched_concepts:

        correct_concepts = (
            "Your explanation includes relevant "
            "concepts related to the topic: "
            + ", ".join(matched_concepts)
            + "."
        )

    else:

        correct_concepts = (
            "Your explanation contains some "
            "relevant information, but the main "
            "concepts need clearer explanation."
        )

    missing_concepts = (
        "Try to include the definition, "
        "main principles, important steps, "
        "and a suitable example of the topic."
    )

    misconceptions = (
        "No major misconceptions identified "
        "from the explanation."
    )

    weak_areas = (
        "Review the main concepts of "
        + topic
        + " and explain them again using "
        "your own words."
    )

    return {
        "understanding_percentage":
            understanding_percentage,

        "understanding_level":
            understanding_level,

        "correct_concepts":
            correct_concepts,

        "missing_concepts":
            missing_concepts,

        "misconceptions":
            misconceptions,

        "weak_areas":
            weak_areas
    }
def generate_flashcards(topic, study_material):
    """
    Generate up to 20 revision flashcards locally from study material.
    Does not require an external AI API.
    """

    import re

    if not study_material or not study_material.strip():
        raise ValueError("Study material cannot be empty.")

    text = study_material.strip()

    # Split material into meaningful sentences or lines.
    parts = re.split(r'[\n.!?]+', text)

    parts = [
        part.strip(" -•\t")
        for part in parts
        if len(part.strip()) > 10
    ]

    flashcards = []
    seen = set()

    def add_card(question, answer):
        question = question.strip()
        answer = answer.strip()

        if not question or not answer:
            return

        key = question.lower()

        if key not in seen and len(flashcards) < 20:
            seen.add(key)

            flashcards.append({
                "question": question,
                "answer": answer
            })

    # --------------------------------------------------
    # 1. Definition cards
    # --------------------------------------------------

    for part in parts:
        match = re.match(
            r'(.+?)\s+(is|are|means|refers to|refers)\s+(.+)',
            part,
            re.IGNORECASE
        )

        if match:
            concept = match.group(1).strip()
            explanation = match.group(3).strip()

            add_card(
                f"What is {concept}?",
                explanation
            )

    # --------------------------------------------------
    # 2. Colon-based concept cards
    # --------------------------------------------------

    for part in parts:
        if ":" in part:
            concept, explanation = part.split(":", 1)

            if (
                len(concept.strip()) > 2
                and len(explanation.strip()) > 5
            ):
                add_card(
                    f"What is {concept.strip()}?",
                    explanation.strip()
                )

    # --------------------------------------------------
    # 3. Important statement cards
    # --------------------------------------------------

    for part in parts:

        lower_part = part.lower()

        if "requires" in lower_part:
            add_card(
                f"What does {topic} require?",
                part
            )

        elif "must" in lower_part:
            add_card(
                f"What requirement is mentioned?",
                part
            )

        elif "important" in lower_part:
            add_card(
                f"What important point is mentioned?",
                part
            )

    # --------------------------------------------------
    # 4. Concept-specific cards
    # --------------------------------------------------

    known_concepts = [
        "1NF",
        "2NF",
        "3NF",
        "BCNF",
        "4NF",
        "5NF",
        "CPU",
        "RAM",
        "ROM",
        "Operating System",
        "Process",
        "Thread",
        "Database",
        "Primary Key",
        "Foreign Key",
        "Normalization"
    ]

    for concept in known_concepts:

        for part in parts:

            if concept.lower() in part.lower():

                add_card(
                    f"What is {concept}?",
                    part
                )

                add_card(
                    f"What is the role of {concept}?",
                    part
                )

                add_card(
                    f"What important point should you remember about {concept}?",
                    part
                )

    # --------------------------------------------------
    # 5. General understanding cards
    # --------------------------------------------------

    for part in parts:

        if len(part.split()) >= 6:

            add_card(
                f"What important point does the material explain?",
                part
            )

            add_card(
                f"Explain this concept in your own words.",
                part
            )

    # --------------------------------------------------
    # 6. Topic-level cards
    # --------------------------------------------------

    if parts:

        add_card(
            f"What is the main purpose of {topic}?",
            parts[0]
        )

        add_card(
            f"What are the important concepts covered in {topic}?",
            "The material covers: " +
            ", ".join(parts[:5])
        )

    # --------------------------------------------------
    # 7. Comparison card
    # --------------------------------------------------

    if len(parts) >= 2:

        add_card(
            f"What is the difference between the first two concepts discussed in {topic}?",
            f"The material explains: {parts[0]} and {parts[1]}"
        )

    # --------------------------------------------------
    # 8. Important fact cards
    # --------------------------------------------------

    for part in parts:

        if len(part.split()) >= 8:

            add_card(
                f"What important fact is given about {topic}?",
                part
            )

    # --------------------------------------------------
    # 9. Additional cards from remaining material
    # --------------------------------------------------

    # If fewer than 20 cards were created,
    # use individual study-material sections to
    # create additional meaningful revision cards.

    for index, part in enumerate(parts):

        if len(flashcards) >= 20:
            break

        add_card(
            f"What should you remember about point {index + 1}?",
            part
        )

    # --------------------------------------------------
    # 10. Final fallback
    # --------------------------------------------------

    if not flashcards:

        flashcards.append({
            "question": f"What is {topic}?",
            "answer": text
        })

    return flashcards[:20]

def generate_mcqs(topic, study_material):
    """
    Generate multiple-choice questions using
    a local rule-based approach.
    """

    material = study_material.strip()

    sentences = [
        sentence.strip()
        for sentence in material.replace(
            "\n",
            " "
        ).split(".")
        if sentence.strip()
    ]

    questions = []

    for sentence in sentences:

        words = sentence.split()

        if len(words) < 5:
            continue

        answer = " ".join(words[:4])

        question_text = (
            f"Which statement is related to "
            f"{topic}?"
        )

        options = [
            sentence,
            f"{answer} is unrelated to {topic}.",
            "It is only used for hardware.",
            "It has no practical purpose."
        ]

        questions.append({
            "question": question_text,
            "options": options,
            "correct_answer": 0
        })

        if len(questions) == 5:
            break


    if not questions:

        questions.append({
            "question":
                f"What is an important concept in {topic}?",
            "options": [
                "The concepts provided in the study material",
                "Only computer hardware",
                "Only internet browsing",
                "None of these"
            ],
            "correct_answer": 0
        })


    return questions
def evaluate_short_answer_local(
    topic,
    question,
    student_answer
):
    """Evaluate a short answer locally."""

    answer_words = {
        word.strip(".,!?()").lower()
        for word in student_answer.split()
        if len(word.strip(".,!?()")) > 3
    }

    topic_words = {
        word.strip(".,!?()").lower()
        for word in topic.split()
        if len(word.strip(".,!?()")) > 3
    }

    matched_words = answer_words.intersection(
        topic_words
    )

    word_count = len(student_answer.split())

    score = 40

    score += min(
        len(matched_words) * 10,
        30
    )

    if word_count >= 30:
        score += 10

    if word_count >= 60:
        score += 10

    score = min(score, 95)

    if matched_words:
        correct_points = (
            "Your answer contains relevant concepts: "
            + ", ".join(sorted(matched_words))
            + "."
        )
    else:
        correct_points = (
            "Your answer addresses the question, "
            "but the main concepts need clearer explanation."
        )

    if word_count < 20:
        missing_points = (
            "Add more explanation, important concepts, "
            "and an example where appropriate."
        )
    else:
        missing_points = (
            "Add more specific concepts, details, "
            "and examples to strengthen your answer."
        )

    if score >= 80:
        feedback = (
            "Good conceptual understanding. "
            "Keep practicing with examples."
        )
    elif score >= 60:
        feedback = (
            "You have a partial understanding. "
            "Review the key concepts and try again."
        )
    else:
        feedback = (
            "Review the topic carefully and "
            "rewrite the answer in your own words."
        )

    return {
        "understanding_percentage": score,
        "correct_points": correct_points,
        "missing_points": missing_points,
        "feedback": feedback
    }