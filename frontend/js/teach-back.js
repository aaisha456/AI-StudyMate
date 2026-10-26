document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("teachBackForm");

    if (!form) {
        return;
    }

    form.addEventListener("submit", analyzeTeachBack);
});


async function analyzeTeachBack(event) {
    event.preventDefault();

    const topicElement = document.getElementById("topic");
    const explanationElement = document.getElementById("explanation");

    const topic = topicElement.value.trim();
    const explanation = explanationElement.value.trim();

    if (!topic || !explanation) {
        alert("Please enter the topic and explain it in your own words.");
        return;
    }

    const submitButton =
        document.querySelector("#teachBackForm button[type='submit']");

    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Analyzing...";
    }

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/ai/teach-back",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({
                    topic: topic,
                    explanation: explanation
                })
            }
        );

        const result = await response.json();

        if (!response.ok || !result.success) {
            alert(result.message || "Unable to analyze your explanation.");
            return;
        }

        displayTeachBackResult(result);

        // Save understanding score to Progress
        await saveUnderstandingProgress(
            result.understanding_percentage
        );

    } catch (error) {
        console.error("Teach Me Back error:", error);
        alert("Unable to connect to StudyMate.");
    } finally {
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = "Analyze My Understanding";
        }
    }
}


function displayTeachBackResult(result) {

    const resultSection =
        document.getElementById("teachBackResult");

    if (resultSection) {
        resultSection.style.display = "block";
    }

    const scoreElement =
        document.getElementById("understandingScore");

    if (scoreElement) {
        scoreElement.textContent =
            `${result.understanding_percentage}%`;
    }

    const levelElement =
        document.getElementById("understandingLevel");

    if (levelElement) {
        levelElement.textContent =
            result.understanding_level || "";
    }

    const correctElement =
        document.getElementById("correctConcepts");

    if (correctElement) {
        correctElement.innerHTML = "";

        (result.correct_concepts || []).forEach(concept => {
            const li = document.createElement("li");
            li.textContent = concept;
            correctElement.appendChild(li);
        });
    }

    const missingElement =
        document.getElementById("missingConcepts");

    if (missingElement) {
        missingElement.innerHTML = "";

        (result.missing_concepts || []).forEach(concept => {
            const li = document.createElement("li");
            li.textContent = concept;
            missingElement.appendChild(li);
        });
    }

    const misconceptionElement =
        document.getElementById("misconceptions");

    if (misconceptionElement) {
        misconceptionElement.innerHTML = "";

        (result.misconceptions || []).forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            misconceptionElement.appendChild(li);
        });
    }

    const weakAreasElement =
        document.getElementById("weakAreas");

    if (weakAreasElement) {
        weakAreasElement.innerHTML = "";

        (result.weak_areas || []).forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            weakAreasElement.appendChild(li);
        });
    }
}


/*
 * Save Teach Me Back understanding score
 * to the student's Progress record.
 */
async function saveUnderstandingProgress(score) {

    const understanding =
        Number(score);

    if (
        Number.isNaN(understanding) ||
        understanding < 0
    ) {
        return;
    }

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/progress/activity",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({
                    activity_type: "understanding",
                    value: understanding
                })
            }
        );

        const result = await response.json();

        if (!response.ok || !result.success) {
            console.error(
                "Unable to save understanding progress:",
                result.message
            );
            return;
        }

        console.log(
            "Understanding progress saved successfully."
        );

    } catch (error) {

        console.error(
            "Progress update error:",
            error
        );
    }
}