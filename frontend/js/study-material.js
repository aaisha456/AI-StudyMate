document.addEventListener("DOMContentLoaded", function () {

    const API_BASE_URL =
        "http://127.0.0.1:5000";


    const studyMaterialForm =
        document.getElementById("studyMaterialForm");

    const materialsContainer =
        document.getElementById("materialsContainer");


    // ==========================================
    // SAVE STUDY MATERIAL
    // ==========================================

    if (studyMaterialForm) {

        studyMaterialForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                const subjectName =
                    document
                        .getElementById("subjectName")
                        .value
                        .trim();


                const topicName =
                    document
                        .getElementById("topicName")
                        .value
                        .trim();


                const materialTitle =
                    document
                        .getElementById("materialTitle")
                        .value
                        .trim();


                const materialContent =
                    document
                        .getElementById("materialContent")
                        .value
                        .trim();


                // Check required fields

                if (
                    !subjectName ||
                    !topicName ||
                    !materialTitle ||
                    !materialContent
                ) {

                    alert(
                        "Please fill in all fields."
                    );

                    return;
                }


                try {

                    const response =
                        await fetch(
                            `${API_BASE_URL}/api/study/materials`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                credentials: "include",

                                body: JSON.stringify({

                                    subject_name:
                                        subjectName,

                                    topic_name:
                                        topicName,

                                    material_title:
                                        materialTitle,

                                    material_content:
                                        materialContent
                                })
                            }
                        );


                    const data =
                        await response.json();


                    if (
                        !response.ok ||
                        !data.success
                    ) {

                        throw new Error(
                            data.message ||
                            "Unable to save study material."
                        );
                    }


                    alert(
                        "Study material saved successfully."
                    );


                    // Clear form

                    studyMaterialForm.reset();


                    // Refresh saved materials

                    await loadStudyMaterials();


                } catch (error) {

                    console.error(
                        "Save material error:",
                        error
                    );


                    alert(
                        error.message ||
                        "Unable to connect to the StudyMate server."
                    );
                }

            }
        );

    }


    // ==========================================
    // LOAD SAVED MATERIALS
    // ==========================================

    async function loadStudyMaterials() {

        if (!materialsContainer) {
            return;
        }


        try {

            const response =
                await fetch(
                    `${API_BASE_URL}/api/study/materials`,
                    {
                        method: "GET",

                        credentials: "include"
                    }
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.message ||
                    "Unable to load study materials."
                );
            }


            // No materials

            if (
                !data.materials ||
                data.materials.length === 0
            ) {

                materialsContainer.innerHTML =
                    `
                    <p class="empty-message">
                        No study materials added yet.
                    </p>
                    `;

                return;
            }


            // Clear old content

            materialsContainer.innerHTML = "";


            // Display each material

            data.materials.forEach(
                function (material) {

                    const materialCard =
                        document.createElement(
                            "article"
                        );


                    materialCard.className =
                        "material-card";


                    materialCard.innerHTML = `

                        <p class="material-subject">
                            ${escapeHtml(
                                material.subject_name
                            )}
                        </p>

                        <h4>
                            ${escapeHtml(
                                material.material_title
                            )}
                        </h4>

                        <p class="material-topic">
                            Topic:
                            ${escapeHtml(
                                material.topic_name
                            )}
                        </p>

                        <p class="material-content">
                            ${escapeHtml(
                                material.material_content
                            )}
                        </p>

                    `;


                    materialsContainer.appendChild(
                        materialCard
                    );

                }
            );


        } catch (error) {

            console.error(
                "Loading materials error:",
                error
            );


            materialsContainer.innerHTML =
                `
                <p class="empty-message">
                    Unable to load study materials.
                </p>
                `;
        }

    }


    // ==========================================
    // ESCAPE HTML
    // ==========================================

    function escapeHtml(value) {

        const element =
            document.createElement("div");


        element.textContent =
            value ?? "";


        return element.innerHTML;
    }


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    loadStudyMaterials();

});