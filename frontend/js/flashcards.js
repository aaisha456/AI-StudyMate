const flashcardTopic =
    document.getElementById("flashcardTopic");

const flashcardQuestion =
    document.getElementById("flashcardQuestion");

const flashcardAnswer =
    document.getElementById("flashcardAnswer");

const showAnswerButton =
    document.getElementById("showAnswerButton");

const nextCardButton =
    document.getElementById("nextCardButton");

const generateFlashcardsButton =
    document.getElementById(
        "generateFlashcardsButton"
    );

const flashcardTopicInput =
    document.getElementById(
        "flashcardTopicInput"
    );

const flashcardMaterialInput =
    document.getElementById(
        "flashcardMaterialInput"
    );

const flashcardGenerationMessage =
    document.getElementById(
        "flashcardGenerationMessage"
    );

const cardsReviewed =
    document.getElementById("cardsReviewed");

const cardsKnown =
    document.getElementById("cardsKnown");

const cardsNeedPractice =
    document.getElementById(
        "cardsNeedPractice"
    );

const cardsUnknown =
    document.getElementById("cardsUnknown");


let flashcards = [];
let currentCardIndex = 0;

let reviewedCount = 0;
let knownCount = 0;
let practiceCount = 0;
let unknownCount = 0;


function displayFlashcard() {

    if (flashcards.length === 0) {
        flashcardTopic.textContent =
            "No flashcards available";

        flashcardQuestion.textContent =
            "Generate flashcards from your study material.";

        flashcardAnswer.textContent = "";

        return;
    }

    const card =
        flashcards[currentCardIndex];

    flashcardTopic.textContent =
        card.topic_name ||
        flashcardTopicInput.value.trim();

    flashcardQuestion.textContent =
        card.question;

    flashcardAnswer.textContent =
        card.answer;

    flashcardAnswer.style.display =
        "none";

    showAnswerButton.textContent =
        "Show Answer";
}


generateFlashcardsButton.addEventListener(
    "click",
    async function () {

        const topic =
            flashcardTopicInput.value.trim();

        const studyMaterial =
            flashcardMaterialInput.value.trim();

        if (!topic || !studyMaterial) {
            alert(
                "Please enter both the topic and study material."
            );
            return;
        }

        generateFlashcardsButton.disabled =
            true;

        generateFlashcardsButton.textContent =
            "Generating...";

        flashcardGenerationMessage.style.display =
            "block";

        flashcardGenerationMessage.textContent =
            "AI is creating your flashcards...";

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/api/ai/flashcards/generate",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "include",

                    body: JSON.stringify({
                        topic: topic,
                        study_material: studyMaterial
                    })
                }
            );

            const result =
                await response.json();

            if (!result.success) {

                flashcardGenerationMessage.textContent =
                    result.message;

                return;
            }

            flashcards =
                result.flashcards.map(
                    function (card) {
                        return {
                            topic_name: result.topic,
                            question: card.question,
                            answer: card.answer
                        };
                    }
                );

            currentCardIndex = 0;

            flashcardGenerationMessage.textContent =
                `${flashcards.length} flashcards generated successfully.`;

            displayFlashcard();

        } catch (error) {

            console.error(
                "Flashcard generation error:",
                error
            );

            flashcardGenerationMessage.textContent =
                "Unable to connect to the AI service.";

        } finally {

            generateFlashcardsButton.disabled =
                false;

            generateFlashcardsButton.textContent =
                "Generate Flashcards";
        }
    }
);


showAnswerButton.addEventListener(
    "click",
    function () {

        if (flashcards.length === 0) {
            return;
        }

        if (
            flashcardAnswer.style.display ===
            "none"
        ) {

            flashcardAnswer.style.display =
                "block";

            showAnswerButton.textContent =
                "Hide Answer";

        } else {

            flashcardAnswer.style.display =
                "none";

            showAnswerButton.textContent =
                "Show Answer";
        }
    }
);


nextCardButton.addEventListener(
    "click",
    function () {

        if (flashcards.length === 0) {
            return;
        }

        currentCardIndex++;

        if (
            currentCardIndex >=
            flashcards.length
        ) {
            currentCardIndex = 0;
        }

        displayFlashcard();
    }
);


const statusButtons =
    document.querySelectorAll(
        "[data-status]"
    );


statusButtons.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                if (flashcards.length === 0) {
                    return;
                }

                const status =
                    button.dataset.status;

                reviewedCount++;

                if (status === "known") {
                    knownCount++;
                }

                if (status === "practice") {
                    practiceCount++;
                }

                if (status === "unknown") {
                    unknownCount++;
                }

                updateProgress();

                moveToNextCard();
            }
        );
    }
);


function updateProgress() {

    cardsReviewed.textContent =
        reviewedCount;

    cardsKnown.textContent =
        knownCount;

    cardsNeedPractice.textContent =
        practiceCount;

    cardsUnknown.textContent =
        unknownCount;
}


function moveToNextCard() {

    currentCardIndex++;

    if (
        currentCardIndex >=
        flashcards.length
    ) {
        currentCardIndex = 0;
    }

    displayFlashcard();
}


displayFlashcard();