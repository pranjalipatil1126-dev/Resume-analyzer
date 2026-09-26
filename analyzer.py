import re

SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "flask",
    "django",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "data science",
    "data analysis",
    "power bi",
    "excel",
    "git",
    "github",
    "mysql",
    "statistics"
]

JOB_ROLES = {
    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "pandas",
        "statistics"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "machine learning",
        "scikit-learn",
        "statistics",
        "sql"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "sql",
        "git"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "python",
        "flask"
    ],

    "ML Engineer": [
        "python",
        "machine learning",
        "scikit-learn",
        "numpy",
        "pandas",
        "git"
    ]
}


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_match(skills, required_skills):
    if not required_skills:
        return 0

    matched = 0

    for skill in required_skills:
        if skill.lower() in [s.lower() for s in skills]:
            matched += 1

    return round((matched / len(required_skills)) * 100)


def recommend_jobs(skills):
    recommendations = []

    for role, required_skills in JOB_ROLES.items():

        score = calculate_match(skills, required_skills)

        missing = [
            skill for skill in required_skills
            if skill.lower() not in [s.lower() for s in skills]
        ]

        recommendations.append({
            "role": role,
            "score": score,
            "missing": missing
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations
