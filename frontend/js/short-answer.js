const shortAnswerForm =
    document.getElementById("shortAnswerForm");

const shortAnswerResult =
    document.getElementById("shortAnswerResult");


shortAnswerForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const topic =
            document
                .getElementById("shortAnswerTopic")
                .value
                .trim();

        const question =
            document
                .getElementById("shortAnswerQuestion")
                .value
                .trim();

        const studentAnswer =
            document
                .getElementById("shortAnswerResponse")
                .value
                .trim();


        if (!topic || !question || !studentAnswer) {

            alert(
                "Please complete all fields."
            );

            return;
        }


        shortAnswerResult.innerHTML = `
            <p class="empty-message">
                Evaluating your answer...
            </p>
        `;


        try {

            const response = await fetch(
                "http://127.0.0.1:5000/api/quiz/short-answer",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "include",

                    body: JSON.stringify({
                        topic: topic,
                        question: question,
                        student_answer: studentAnswer
                    })
                }
            );


            const result =
                await response.json();


            if (!result.success) {

                shortAnswerResult.innerHTML = `
                    <p class="empty-message">
                        ${escapeHtml(result.message)}
                    </p>
                `;

                return;
            }


            displayEvaluation(
                result.evaluation
            );


        } catch (error) {

            console.error(
                "Short answer error:",
                error
            );

            shortAnswerResult.innerHTML = `
                <p class="empty-message">
                    Unable to connect to the StudyMate server.
                </p>
            `;
        }
    }
);


function displayEvaluation(evaluation) {

    shortAnswerResult.innerHTML = `

        <article class="material-card">

            <p class="material-subject">
                UNDERSTANDING SCORE
            </p>

            <h4>
                ${escapeHtml(
                    String(evaluation.understanding_percentage)
                )}%
            </h4>

        </article>


        <article class="material-card">

            <p class="material-subject">
                WHAT YOU DID WELL
            </p>

            <p class="material-content">
                ${escapeHtml(
                    evaluation.correct_points
                )}
            </p>

        </article>


        <article class="material-card">

            <p class="material-subject">
                WHAT IS MISSING
            </p>

            <p class="material-content">
                ${escapeHtml(
                    evaluation.missing_points
                )}
            </p>

        </article>


        <article class="material-card">

            <p class="material-subject">
                FEEDBACK
            </p>

            <p class="material-content">
                ${escapeHtml(
                    evaluation.feedback
                )}
            </p>

        </article>

    `;
}


function escapeHtml(value) {

    const temporaryElement =
        document.createElement("div");

    temporaryElement.textContent =
        value ?? "";

    return temporaryElement.innerHTML;
}