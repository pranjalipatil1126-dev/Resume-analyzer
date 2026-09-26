from flask import Flask, render_template, request
from pypdf import PdfReader
from analyzer import extract_skills, recommend_jobs
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_pdf_text(filepath):

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return "No resume uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume"

    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF resumes are supported"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    text = extract_pdf_text(filepath)

    skills = extract_skills(text)

    recommendations = recommend_jobs(skills)

    return render_template(
        "result.html",
        skills=skills,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)
