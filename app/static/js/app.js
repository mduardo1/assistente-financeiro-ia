document.addEventListener("DOMContentLoaded", () => {
    const firstInput = document.querySelector("input, textarea, select");

    if (firstInput) {
        firstInput.focus();
    }
});
