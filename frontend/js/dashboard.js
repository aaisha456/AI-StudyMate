document.addEventListener("DOMContentLoaded", loadCurrentUser);

async function loadCurrentUser() {
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/auth/me",
            {
                method: "GET",
                credentials: "include"
            }
        );

        const result = await response.json();

        if (!result.success) {
            window.location.href = "login.html";
            return;
        }

        const welcomeHeading = document.querySelector(".dashboard-welcome h2");

        if (welcomeHeading) {
            welcomeHeading.textContent =
                `Welcome, ${result.user.full_name}`;
        }

    } catch (error) {
        console.error("Dashboard user error:", error);
    }
}
async function loadProgress() {
    console.log("loadProgress started");
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/progress",
            {
                method: "GET",
                credentials: "include"
            }
        );

        const result = await response.json();

        if (!result.success) {
            return;
        }

        console.log("Progress data:", result.progress);
        document.getElementById("topicsStudied").textContent =
    result.progress.topics_studied;

document.getElementById("conceptsPracticed").textContent =
    result.progress.concepts_practiced;

document.getElementById("flashcardsReviewed").textContent =
    result.progress.flashcards_reviewed;

document.getElementById("understandingPercentage").textContent =
    `${result.progress.understanding_percentage}%`;
document.getElementById("revisionTopicCount").textContent =
    result.progress.revision_topic_count ?? 0;
console.log("Revision count:", result.progress.revision_topic_count);
console.log("Revision element:", document.getElementById("revisionTopicCount"));
document.getElementById("revisionStatus").textContent =
    (result.progress.revision_topic_count ?? 0) > 0
        ? "Recommended"
        : "On Track";
    } catch (error) {
        console.error("Progress loading error:", error);
    }
}
loadProgress();