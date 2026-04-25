document.addEventListener("DOMContentLoaded", () => {
    const firstInput = document.querySelector("input, textarea, select");

    if (firstInput) {
        firstInput.focus();
    }

    const forms = document.querySelectorAll("[data-loading-form]");

    forms.forEach((form) => {
        form.addEventListener("submit", () => {
            const submitButton = form.querySelector("button[type='submit']");

            if (!submitButton || submitButton.disabled) {
                return;
            }

            submitButton.dataset.originalText = submitButton.textContent;
            submitButton.textContent = submitButton.dataset.loadingText || "Salvando...";
            submitButton.disabled = true;
            submitButton.classList.add("is-loading");
        });
    });
});
