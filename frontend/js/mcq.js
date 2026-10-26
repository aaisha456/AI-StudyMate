const mcqForm =
    document.getElementById("mcqForm");

const mcqContainer =
    document.getElementById("mcqContainer");


mcqForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const topic =
            document
                .getElementById("mcqTopic")
                .value
                .trim();

        const studyMaterial =
            document
                .getElementById("mcqMaterial")
                .value
                .trim();


        if (!topic || !studyMaterial) {

            alert(
                "Please enter the topic and study material."
            );

            return;
        }


        mcqContainer.innerHTML = `
            <p class="empty-message">
                Generating practice questions...
            </p>
        `;


        try {

            const response = await fetch(
                "http://127.0.0.1:5000/api/quiz/generate",
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

                mcqContainer.innerHTML = `
                    <p class="empty-message">
                        ${escapeHtml(result.message)}
                    </p>
                `;

                return;
            }


            displayQuestions(
                result.questions
            );


        } catch (error) {

            console.error(
                "MCQ error:",
                error
            );

            mcqContainer.innerHTML = `
                <p class="empty-message">
                    Unable to connect to the StudyMate server.
                </p>
            `;
        }
    }
);


function displayQuestions(questions) {

    mcqContainer.innerHTML = "";


    questions.forEach(
        function (question, index) {

            const questionCard =
                document.createElement("article");

            questionCard.className =
                "material-card";


            questionCard.innerHTML = `

                <p class="material-subject">
                    QUESTION ${index + 1}
                </p>

                <h4>
                    ${escapeHtml(question.question)}
                </h4>

                <div class="mcq-options">

                    ${question.options.map(
                        function (option, optionIndex) {

                            return `
                                <label>
                                    <input
                                        type="radio"
                                        name="question-${index}"
                                        value="${optionIndex}"
                                    >

                                    ${escapeHtml(option)}
                                </label>
                            `;
                        }
                    ).join("")}

                </div>

            `;


            mcqContainer.appendChild(
                questionCard
            );
        }
    );


    const submitButton =
        document.createElement("button");

    submitButton.type = "button";

    submitButton.className =
        "primary-button";

    submitButton.textContent =
        "Submit Answers";


    submitButton.addEventListener(
        "click",
        function () {

            calculateScore(questions);

        }
    );


    mcqContainer.appendChild(
        submitButton
    );
}


function calculateScore(questions) {

    let score = 0;


    questions.forEach(
        function (question, index) {

            const selected =
                document.querySelector(
                    `input[name="question-${index}"]:checked`
                );


            if (
                selected &&
                Number(selected.value) ===
                Number(question.correct_answer)
            ) {

                score++;
            }
        }
    );


    const percentage =
        Math.round(
            (score / questions.length) * 100
        );


    const resultMessage =
        document.createElement("div");

    resultMessage.className =
        "material-card";


    resultMessage.innerHTML = `

        <p class="material-subject">
            PRACTICE RESULT
        </p>

        <h4>
            ${score} / ${questions.length}
        </h4>

        <p class="material-content">
            Your score is ${percentage}%.
        </p>

    `;


    mcqContainer.prepend(
        resultMessage
    );
}


function escapeHtml(value) {

    const temporaryElement =
        document.createElement("div");

    temporaryElement.textContent =
        value ?? "";

    return temporaryElement.innerHTML;
}
