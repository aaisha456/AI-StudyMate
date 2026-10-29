document.addEventListener(
    "DOMContentLoaded",
    loadRevisionData
);

async function loadRevisionData() {
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

        const revisionCount =
            Number(result.progress.revision_topic_count) || 0;

        const revisionTopicCount =
            document.getElementById("revisionTopicCount");

        const revisionStatus =
            document.getElementById("revisionStatus");

        if (revisionTopicCount) {
            revisionTopicCount.textContent = revisionCount;
        }

        if (revisionStatus) {
            revisionStatus.textContent =
                revisionCount > 0 ? "Recommended" : "On Track";
        }

    } catch (error) {
        console.error("Smart Revision error:", error);
    }
}