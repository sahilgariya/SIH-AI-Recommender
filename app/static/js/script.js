const form =
    document.getElementById(
        "recommendationForm"
    );


const submitButton =
    document.getElementById(
        "submitButton"
    );


if (form) {

    form.addEventListener(
        "submit",
        function () {

            submitButton.disabled = true;

            submitButton.textContent =
                "Finding Best Problems...";

        }
    );

}