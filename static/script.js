const form = document.querySelector("form");

if (form) {

    form.addEventListener("submit", function () {

        const button = form.querySelector("button");

        button.innerText = "Analyzing Resume...";

        button.disabled = true;

    });

}
