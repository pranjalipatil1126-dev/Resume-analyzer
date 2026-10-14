document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("resumeForm");
    const fileInput = document.getElementById("resume");
    const analyzeButton = document.getElementById("analyzeButton");

    if (!form || !fileInput || !analyzeButton) {
        return;
    }

    form.addEventListener("submit", function (event) {
        if (!fileInput.files.length) {
            event.preventDefault();
            alert("Please select a PDF resume first.");
            return;
        }

        const file = fileInput.files[0];

        if (!file.name.toLowerCase().endsWith(".pdf")) {
            event.preventDefault();
            alert("Please select a PDF file.");
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            event.preventDefault();
            alert("Your PDF must be smaller than 10 MB.");
            return;
        }

        analyzeButton.disabled = true;
        analyzeButton.innerHTML = "Analyzing Resume... Please wait";
    });
});