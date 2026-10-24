
import streamlit as st

st.set_page_config(
    page_title="Student Placement Finder",
    page_icon="🎓"
)

jobs = [
    {
        "company": "TechNova",
        "role": "Python Developer",
        "branch": ["Computer", "IT", "EXTC"],
        "cgpa": 7.0,
        "skills": ["python", "sql", "dsa"]
    },
    {
        "company": "ElectroTech",
        "role": "Embedded Engineer",
        "branch": ["EXTC", "Electrical"],
        "cgpa": 6.5,
        "skills": ["c", "arduino", "embedded c"]
    },
    {
        "company": "DataWorks",
        "role": "Data Analyst",
        "branch": ["Computer", "IT", "EXTC",
                   "Electrical", "Mechanical"],
        "cgpa": 7.0,
        "skills": ["python", "sql", "excel"]
    },
    {
        "company": "CircuitPro",
        "role": "Electronics Engineer",
        "branch": ["EXTC", "Electrical"],
        "cgpa": 6.0,
        "skills": ["c", "electronics", "arduino"]
    },
    {
        "company": "WebSpark",
        "role": "Web Developer",
        "branch": ["Computer", "IT", "EXTC"],
        "cgpa": 6.0,
        "skills": ["html", "css", "javascript"]
    }
]


def find_jobs(branch, cgpa, student_skills, role):
    results = []

    # Linear search and filtering
    for job in jobs:
        if branch not in job["branch"]:
            continue

        if cgpa < job["cgpa"]:
            continue

        if role != "All Roles" and role != job["role"]:
            continue

        matched = [
            skill for skill in student_skills
            if skill in job["skills"]
        ]

        score = round(
            len(matched) / len(job["skills"]) * 100
        )

        result = job.copy()
        result["matched"] = matched
        result["score"] = score
        results.append(result)

    # Bubble sort by skill-match score
    n = len(results)

    for i in range(n):
        for j in range(n - i - 1):
            if results[j]["score"] < results[j + 1]["score"]:
                results[j], results[j + 1] = (
                    results[j + 1], results[j]
                )

    return results


st.title("🎓 Student Placement Finder")
st.write(
    "Find suitable placement opportunities based on "
    "your branch, CGPA and technical skills."
)

st.divider()

st.subheader("Enter Your Details")

name = st.text_input("Student Name")

branch = st.selectbox(
    "Engineering Branch",
    ["EXTC", "Computer", "IT", "Electrical", "Mechanical"]
)

cgpa = st.number_input(
    "Your CGPA",
    min_value=0.0,
    max_value=10.0,
    value=7.0,
    step=0.1
)

skills_text = st.text_input(
    "Your Skills",
    placeholder="python, c, arduino"
)

role = st.selectbox(
    "Preferred Job Role",
    [
        "All Roles",
        "Python Developer",
        "Embedded Engineer",
        "Data Analyst",
        "Electronics Engineer",
        "Web Developer"
    ]
)

if st.button("Find Suitable Placements"):
    if not name.strip():
        st.warning("Please enter your name.")
    else:
        student_skills = [
            skill.strip().lower()
            for skill in skills_text.split(",")
            if skill.strip()
        ]

        results = find_jobs(
            branch, cgpa, student_skills, role
        )

        st.subheader("Placement Results")
        st.write("Student:", name)

        if not results:
            st.info("No suitable jobs found.")
        else:
            st.success(
                str(len(results)) + " suitable job(s) found."
            )

            for job in results:
                with st.container(border=True):
                    st.subheader(job["role"])
                    st.write("Company:", job["company"])
                    st.write("Eligible Branches:",
                             ", ".join(job["branch"]))
                    st.write("Minimum CGPA:", job["cgpa"])
                    st.write("Required Skills:",
                             ", ".join(job["skills"]))
                    st.write("Matching Skills:",
                             ", ".join(job["matched"])
                             if job["matched"] else "None")
                    st.progress(job["score"] / 100)
                    st.write(
                        "Skill Match Score:",
                        str(job["score"]) + "%"
                    )

st.divider()
st.caption(
    "Academic project | Sample placement data only"
)
