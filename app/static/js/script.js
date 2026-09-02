const form = document.getElementById("recommendationForm");
const submitButton = document.getElementById("submitButton");
const input = document.getElementById("user_input");

if (form && submitButton && input) {
    form.addEventListener("submit", function (event) {
        const value = input.value.trim();

        if (!value) {
            event.preventDefault();
            input.focus();
            return;
        }

        if (value.length > 500) {
            event.preventDefault();
            alert("Please keep your input under 500 characters.");
            input.focus();
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Finding Best Problems...";
    });
}
