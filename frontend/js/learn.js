const learnForm =
    document.getElementById("learnForm");

const aiExplanationContainer =
    document.getElementById("aiExplanationContainer");


/* =========================================
   GENERATE AI EXPLANATION
   ========================================= */

if (learnForm) {

    learnForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const topic =
                document.getElementById("learnTopic")
                    .value
                    .trim();

            const studyMaterial =
                document.getElementById("learnMaterial")
                    .value
                    .trim();


            /* -----------------------------------------
               VALIDATION
            ----------------------------------------- */

            if (!topic || !studyMaterial) {

                alert(
                    "Please enter both the topic and study material."
                );

                return;
            }


            /* -----------------------------------------
               LOADING MESSAGE
            ----------------------------------------- */

            aiExplanationContainer.innerHTML = `
                <p class="empty-message">
                    StudyMate is preparing your explanation...
                </p>
            `;


            try {

                const response = await fetch(
                    "http://127.0.0.1:5000/api/ai/explain",
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


                /* -----------------------------------------
                   CHECK SERVER RESPONSE
                ----------------------------------------- */

                const result =
                    await response.json();


                if (!response.ok || !result.success) {

                    aiExplanationContainer.innerHTML = `
                        <p class="empty-message">
                            ${escapeHtml(
                                result.message ||
                                "Unable to generate explanation."
                            )}
                        </p>
                    `;

                    return;
                }


                /* -----------------------------------------
                   DISPLAY EXPLANATION
                ----------------------------------------- */

                aiExplanationContainer.innerHTML = `
                    <article class="material-card">

                        <p class="material-subject">
                            STUDYMATE EXPLANATION
                        </p>

                        <h4>
                            ${escapeHtml(result.topic)}
                        </h4>

                        <div class="material-content explanation-content">
                            ${formatExplanation(
                                result.explanation
                            )}
                        </div>

                    </article>
                `;

            }

            catch (error) {

                console.error(
                    "AI explanation error:",
                    error
                );

                aiExplanationContainer.innerHTML = `
                    <p class="empty-message">
                        Unable to connect to the StudyMate server.
                        Please make sure the Flask backend is running.
                    </p>
                `;
            }

        }
    );

}


/* =========================================
   FORMAT EXPLANATION
   ========================================= */

function formatExplanation(text) {

    if (!text) {
        return "";
    }

    const escapedText =
        escapeHtml(text);

    return escapedText
        .replace(/\n\n/g, "<br><br>")
        .replace(/\n/g, "<br>");
}


/* =========================================
   BASIC HTML ESCAPING
   ========================================= */

function escapeHtml(value) {

    const temporaryElement =
        document.createElement("div");

    temporaryElement.textContent =
        value ?? "";

    return temporaryElement.innerHTML;
}