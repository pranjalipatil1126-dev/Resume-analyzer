from flask import Flask, render_template, request
from pypdf import PdfReader
from analyzer import extract_skills, recommend_jobs
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_pdf_text(filepath):
    """Extract text from all pages of a PDF."""
    reader = PdfReader(filepath)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check whether a file was submitted.
    if "resume" not in request.files:
        return render_template(
            "index.html",
            error="Please select a resume PDF before submitting."
        )

    file = request.files["resume"]

    # Check whether the user selected a file.
    if not file or file.filename == "":
        return render_template(
            "index.html",
            error="No file selected. Please choose a PDF resume."
        )

    # Check the file extension.
    if not allowed_file(file.filename):
        return render_template(
            "index.html",
            error="Invalid file type. Please upload a PDF."
        )

    filename = secure_filename(file.filename)

    if not filename:
        return render_template(
            "index.html",
            error="Invalid filename. Please choose another PDF."
        )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    try:
        # Save the uploaded PDF.
        file.save(filepath)

        # Extract the resume text.
        text = extract_pdf_text(filepath)

        if not text.strip():
            return render_template(
                "index.html",
                error=(
                    "No readable text was found in this PDF. "
                    "Try a text-based PDF instead of a scanned image."
                )
            )

        # Detect skills.
        skills = extract_skills(text)

        # Recommend suitable job roles.
        recommendations = recommend_jobs(skills)

        print("\nResume uploaded successfully.")
        print("Extracted text length:", len(text))
        print("Detected skills:", skills)
        print("Recommended roles:", len(recommendations))

        # Display the results.
        return render_template(
            "result.html",
            skills=skills,
            recommendations=recommendations
        )

    except Exception as e:
        app.logger.exception("Resume analysis failed")

        return render_template(
            "index.html",
            error=f"Could not analyze the PDF: {str(e)}"
        )

    finally:
        # Remove the uploaded file after analysis.
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                app.logger.warning("Could not remove uploaded PDF.")


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error="The PDF is too large. Please upload a file smaller than 10 MB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)