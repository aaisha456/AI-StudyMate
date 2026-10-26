const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const result = await response.json();

        if (result.success) {
            alert(result.message);

            // Go to dashboard after successful login
            window.location.href = "dashboard.html";
        } else {
            alert(result.message);
        }

    } catch (error) {
        console.error("Login error:", error);
        alert("Unable to connect to the server. Please try again.");
    }
});

const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", function () {

        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePassword.textContent = "🙈";
            togglePassword.setAttribute("aria-label", "Hide password");
        } else {
            passwordInput.type = "password";
            togglePassword.textContent = "👁";
            togglePassword.setAttribute("aria-label", "Show password");
        }

    });
}       