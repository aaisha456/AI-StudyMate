document.addEventListener(
    "DOMContentLoaded",
    loadProgress
);


/* =========================================
   LOAD PROGRESS
========================================= */

async function loadProgress() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/progress",
            {
                method: "GET",
                credentials: "include"
            }
        );


        const result =
            await response.json();


        /* -----------------------------------------
           CHECK RESPONSE
        ----------------------------------------- */

        if (!response.ok || !result.success) {

            console.error(
                "Progress error:",
                result.message || "Unable to load progress."
            );

            return;
        }


        /* -----------------------------------------
           IMPORTANT:
           Progress data is inside result.progress
        ----------------------------------------- */

        const progress =
            result.progress || {};


        const topicsStudied =
            Number(
                progress.topics_studied
            ) || 0;


        const conceptsPracticed =
            Number(
                progress.concepts_practiced
            ) || 0;


        const flashcardsReviewed =
            Number(
                progress.flashcards_reviewed
            ) || 0;


        const understanding =
            Number(
                progress.understanding_percentage
            ) || 0;


        /* -----------------------------------------
           UPDATE TOPICS STUDIED
        ----------------------------------------- */

        const topicsElement =
            document.getElementById(
                "topicsStudied"
            );

        if (topicsElement) {

            topicsElement.textContent =
                topicsStudied;
        }


        /* -----------------------------------------
           UPDATE CONCEPTS PRACTICED
        ----------------------------------------- */

        const conceptsElement =
            document.getElementById(
                "conceptsPracticed"
            );

        if (conceptsElement) {

            conceptsElement.textContent =
                conceptsPracticed;
        }


        /* -----------------------------------------
           UPDATE FLASHCARDS REVIEWED
        ----------------------------------------- */

        const flashcardsElement =
            document.getElementById(
                "flashcardsReviewed"
            );

        if (flashcardsElement) {

            flashcardsElement.textContent =
                flashcardsReviewed;
        }


        /* -----------------------------------------
           UPDATE UNDERSTANDING PERCENTAGE
        ----------------------------------------- */

        const understandingElement =
            document.getElementById(
                "understandingPercentage"
            );

        if (understandingElement) {

            understandingElement.textContent =
                understanding;
        }


        /* -----------------------------------------
           UPDATE PROGRESS BAR
        ----------------------------------------- */

        const understandingBar =
            document.getElementById(
                "understandingBar"
            );

        if (understandingBar) {

            understandingBar.style.width =
                understanding + "%";
        }


        /* -----------------------------------------
           UPDATE MESSAGE
        ----------------------------------------- */

        updateUnderstandingMessage(
            understanding
        );


    } catch (error) {

        console.error(
            "Unable to load progress:",
            error
        );

    }

}


/* =========================================
   UNDERSTANDING MESSAGE
========================================= */

function updateUnderstandingMessage(
    percentage
) {

    const message =
        document.getElementById(
            "understandingMessage"
        );


    if (!message) {
        return;
    }


    if (percentage >= 80) {

        message.textContent =
            "Good progress. Keep practicing to strengthen your understanding.";

    }

    else if (percentage >= 60) {

        message.textContent =
            "You have a developing understanding. Review weak areas and practice again.";

    }

    else if (percentage > 0) {

        message.textContent =
            "Your understanding needs more practice. Review your study material and try again.";

    }

    else {

        message.textContent =
            "Start practicing to build your learning progress.";

    }

}