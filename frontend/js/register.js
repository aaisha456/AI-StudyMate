const registerForm = document.getElementById("registerForm");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const fullName = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Check whether passwords match
    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/auth/register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    full_name: fullName,
                    email: email,
                    password: password
                })
            }
        );

        const result = await response.json();

        if (response.ok) {
            alert(result.message);

            // Send the user to the login page
            window.location.href = "./login.html";
        } else {
            alert(result.message);
        }

    } catch (error) {
        console.error("Registration error:", error);
        alert("Unable to connect to the server. Please try again.");
    }
});

const toggleRegisterPassword =
    document.getElementById("toggleRegisterPassword");

const registerPasswordInput =
    document.getElementById("password");

if (toggleRegisterPassword && registerPasswordInput) {

    toggleRegisterPassword.addEventListener("click", function () {

        if (registerPasswordInput.type === "password") {

            registerPasswordInput.type = "text";
            toggleRegisterPassword.textContent = "🙈";
            toggleRegisterPassword.setAttribute(
                "aria-label",
                "Hide password"
            );

        } else {

            registerPasswordInput.type = "password";
            toggleRegisterPassword.textContent = "👁";
            toggleRegisterPassword.setAttribute(
                "aria-label",
                "Show password"
            );

        }

    });

}