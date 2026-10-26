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


        const result =
            await response.json();


        if (!result.success) {
            return;
        }


        const understanding =
            Number(
                result.understanding_percentage
            ) || 0;


        const topicCount =
            Number(
                result.topics_studied
            ) || 0;


        const revisionTopicCount =
            document.getElementById(
                "revisionTopicCount"
            );


        const revisionStatus =
            document.getElementById(
                "revisionStatus"
            );


        /*
         * If understanding is below 80%,
         * revision is recommended.
         */

        if (understanding < 80) {

            revisionTopicCount.textContent =
                topicCount;

            revisionStatus.textContent =
                "Recommended";

        } else {

            revisionTopicCount.textContent =
                0;

            revisionStatus.textContent =
                "On Track";

        }


    } catch (error) {

        console.error(
            "Smart Revision error:",
            error
        );

    }

}