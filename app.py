from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"

YEAR_GROUPS = [
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "Others",
]

SUBJECTS = [
    "Mathematics",
    "English",
    "Science",
    "History",
    "Geography",
    "Coding",
    "Japanese",
    "Chinese",
    "Commerce",
]

CORE = {
    year: ["Mathematics", "English", "Science", "History", "Geography"]
    for year in YEAR_GROUPS
}

ELECTIVE = {year: ["Coding", "Japanese", "Chinese", "Commerce"] for year in YEAR_GROUPS}

CORE_FILES = {
    "5": {
        "Mathematics": [
            {
                "title": "Year 5 Maths - Mental division questions",
                "filename": "files/core/5/mathematics/div5.pdf",
            }
        ],
        "English": [
            {
                "title": "Year 5 English - After the Flood",
            }
        ],
        "Science": [
            {
                "title": "Year 5 Science - Glass animals - biology",
            }
        ],
        "Geography": [
            {
                "title": "Year 5 Geography - Basic geographic skill quiz",
            }
        ],
        "History": [
            {
                "title": "Year 5 History - Aboriginal and European contact worksheet",
            }
        ],
    },
    "6": {
        "Mathematics": [
            {
                "title": "Year 6 Maths - Perimeter and Area mini test",
            }
        ],
        "English": [
            {
                "title": "Year 6 English - Grammar and figurative language skills",
            }
        ],
        "Science": [
            {
                "title": "Year 6 Science - Periodic Table",
            }
        ],
        "Geography": [
            {
                "title": "Year 6 Geography - Australia and Asia",
            }
        ],
        "History": [
            {
                "title": "Year 6 History - History of Australia's Parliament House",
            }
        ],
    },
    "7": {
        "Mathematics": [{"title": "Year 7 Maths - Linear relationship Test"}],
        "English": [
            {
                "title": "Year 7 English - Introduction to Shakespeare",
            }
        ],
        "Science": [
            {
                "title": "Year 7 Science - Circuit and electricity notes",
            }
        ],
        "Geography": [
            {
                "title": "Year 7 Geography - Flood; reading activity ",
            }
        ],
        "History": [
            {
                "title": "Year 7 History - Ancient China vocabulary ",
            }
        ],
    },
    "8": {
        "Mathematics": [
            {
                "title": "Year 8 Maths - Fill in the blank; Trigonometry",
            }
        ],
        "English": [
            {
                "title": "Year 8 English - Essay writing practice exam",
            }
        ],
        "Science": [
            {
                "title": "Year 8 Science - Ecosystem information",
            }
        ],
        "Geography": [
            {
                "title": "Year 8 Geography - Map skills",
            }
        ],
        "History": [
            {
                "title": "Year 8 History - Black Death worksheet",
            }
        ],
    },
    "9": {
        "Mathematics": [
            {
                "title": "Year 9 Maths - Linear Relationships Test",
                "filename": "files/core/9/mathematics/linear7.pdf",
            }
        ],
        "English": [
            {
                "title": "Year 9 English - The Monkey's Paw",
            }
        ],
        "Science": [
            {
                "title": "Year 9 Science - Practice questions of drawing circuits",
            }
        ],
        "Geography": [
            {
                "title": "Year 9 Geography - Water Cycle worksheet",
            }
        ],
        "History": [
            {
                "title": "Year 9 History - Earth history quiz",
            }
        ],
    },
    "10": {
        "Mathematics": [
            {
                "title": "Year 10 Maths - Parabola and Rates of Change revision",
            }
        ],
        "English": [
            {
                "title": "Year 10 English - Romeo and Juliet workbook",
            }
        ],
        "Science": [
            {
                "title": "Year 10 Science - Chemistry notes",
            }
        ],
        "Geography": [
            {
                "title": "Year 10 Geography - Gradient skills",
            }
        ],
        "History": [
            {
                "title": "Year 10 History - History exam: Questions ",
            },
            {
                "title": "Year 10 History - History exam: Source ",
            },
        ],
    },
    "11": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Advanced Trigonometric Equations",
            }
        ],
        "English": [
            {
                "title": "Year 11 English - Sample Essay of Never Let Me Go and Blade Runner",
            }
        ],
        "Science": [
            {
                "title": "Year 11 Science - Biology Revision",
            }
        ],
        "Geography": [
            {
                "title": "Year 11 Geography - Asian Geography",
            }
        ],
        "History": [
            {
                "title": "Year 11 History - Sample end of year exam paper",
            }
        ],
    },
    "12": {
        "Mathematics": [
            {
                "title": "Year 12 Maths - Extension 1 HSC 2025",
                "url": "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/mathematics-extension-1/2025",
            }
        ],
        "English": [
            {
                "title": "Year 12 English - Advanced paper 1 HSC 2024 ",
                "url": "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/english-advanced/2024",
            }
        ],
        "Science": [
            {
                "title": "Year 12 Science - Physics HSC 2024",
                "url": "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/physics/2024",
            }
        ],
        "Geography": [
            {
                "title": "Year 12 Geography - Geography HSC 2025",
                "url": "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/geography/2025",
            }
        ],
        "History": [
            {
                "title": "Year 12 History - Modern History HSC 2025",
                "url": "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/modern-history/2025",
            }
        ],
    },
    "Others": {},
}

ELECTIVE_FILES = {
    "7": {
        "Coding": [
            {
                "title": "Year 7 Coding - PC component terminology quiz",
                "filename": "files/elective/7/coding/code7.pdf",
            }
        ],
        "Japanese": [
            {
                "title": "Year 7 Japanese - Family vocabulary worksheet",
            }
        ],
        "Chinese": [
            {
                "title": "Year 7 Chinese - Sample assessment task; Family",
            }
        ],
        "Commerce": [
            {
                "title": "Year 7 Commerce - Economy quiz ",
            }
        ],
    },
    "8": {
        "Coding": [
            {
                "title": "Year 8 Coding - Computer Science Terminology",
            }
        ],
        "Japanese": [
            {
                "title": "Year 8 Japanese - Revision quiz ",
            }
        ],
        "Chinese": [
            {
                "title": "Year 8 Chinese - Describing appearance worksheet ",
            }
        ],
        "Commerce": [
            {
                "title": "Year 8 Commerce - Business and Economic Commerce",
            }
        ],
    },
    "9": {
        "Coding": [
            {
                "title": "Year 9 Coding - CipherForge",
                "url": "https://hsc-software-engineering.onrender.com/learning/flask-encryption-algorithm/",
            }
        ],
        "Japanese": [
            {
                "title": "Year 9 Japanese - New Japanese-Language Proficiency Test Sample Questions - N5",
                "url": "https://www.jlpt.jp/e/samples/n5/index.html",
            }
        ],
        "Chinese": [
            {
                "title": "Year 9 Chinese - Pinyin understanding quiz",
            }
        ],
        "Commerce": [
            {
                "title": "Year 9 Commerce - Commercial Year 9 Textbook",
            }
        ],
    },
    "10": {
        "Coding": [
            {
                "title": "Year 10 Coding - Game Design Theory",
                "url": "https://hsc-software-engineering.onrender.com/learning/game-design-theory/",
            }
        ],
        "Japanese": [
            {
                "title": "Year 10 Japanese - Sample assessment task; School life ",
            }
        ],
        "Chinese": [
            {
                "title": "Year 10 Chinese - Vocabulary Quiz",
            }
        ],
        "Commerce": [
            {
                "title": "Year 10 Commerce - Commerce Yearly Exam Revision",
            }
        ],
    },
    "11": {
        "Coding": [
            {
                "title": "Year 11 Coding - Algorithm Design",
            }
        ],
        "Japanese": [
            {
                "title": "Year 11 Japanese - New Japanese-Language Proficiency Test Sample Questions - N4",
                "url": "",
            }
        ],
        "Chinese": [
            {
                "title": "Year 11 Chinese - 2024 HSC Beginners Exam Paper",
                "url": "https://www.jlpt.jp/e/samples/n4/index.html",
            }
        ],
        "Commerce": [
            {
                "title": "Year 11 Commerce - Business Review worksheet",
            }
        ],
    },
    "12": {
        "Coding": [
            {
                "title": "Year 12 Coding - HSC examination",
                "url": "https://fam.hsconline.nesa.nsw.edu.au/",
            }
        ],
        "Japanese": [
            {
                "title": "Year 12 Japanese - New Japanese-Language Proficiency Test Sample Questions - N3",
                "url": "https://www.jlpt.jp/e/samples/n3/index.html",
            }
        ],
        "Chinese": [
            {
                "title": "Year 12 Chinese - 2025 HSC Continuers Exam Paper",
                "url": "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/chinese-continuers/2025",
            }
        ],
        "Commerce": [
            {
                "title": "Year 12 Commerce - 2025 HSC Business Studies examination",
                "url": "https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers/business-studies/2025",
            }
        ],
    },
    "Others": {},
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match.")

        session["name"] = name
        session.pop("year_group", None)
        return redirect(url_for("userform"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not password:
            return render_template(
                "login.html", error="Please enter name and password."
            )

        session["name"] = name

        if session.get("year_group"):
            return redirect(url_for("userprivate"))
        return redirect(url_for("userform"))

    return render_template("login.html")


@app.route("/userform", methods=["GET", "POST"])
def userform():
    name = session.get("name", "User")
    if request.method == "POST":
        year_group = request.form.get("year_group", "")
        if year_group not in YEAR_GROUPS:
            return render_template(
                "userform.html",
                name=name,
                year_groups=YEAR_GROUPS,
                selected_year=session.get("year_group", ""),
                error="Please select a valid year group.",
            )
        session["year_group"] = year_group
        return redirect(url_for("userprivate"))

    return render_template(
        "userform.html",
        name=name,
        year_groups=YEAR_GROUPS,
        selected_year=session.get("year_group", ""),
    )


@app.route("/userprivate")
def userprivate():
    name = session.get("name", "User")
    year_group = session.get("year_group")
    if not year_group:
        return redirect(url_for("userform"))
    return render_template("userprivate.html", name=name, year_group=year_group)


@app.route("/core", methods=["GET", "POST"])
def core():
    if request.method == "POST":
        selected_year = request.form.get("year_group", "")
        if selected_year in YEAR_GROUPS:
            session["year_group"] = selected_year
        return redirect(url_for("core"))

    year_group = session.get("year_group")
    if not year_group:
        return redirect(url_for("userform"))

    subjects = CORE.get(year_group, [])

    if year_group == "Others":
        core_files = {}
        for year, year_data in CORE_FILES.items():
            if year == "Others":
                continue
            for subject, files in year_data.items():
                core_files.setdefault(subject, [])
                for f in files:
                    core_files[subject].append(
                        {
                            "title": f"[Year {year}] {f['title']}",
                            "filename": f["filename"],
                        }
                    )
    else:
        core_files = CORE_FILES.get(year_group, {})

    return render_template(
        "core.html",
        year_group=year_group,
        year_groups=YEAR_GROUPS,
        subjects=subjects,
        core_files=core_files,
    )


@app.route("/elective", methods=["GET", "POST"])
def elective():
    if request.method == "POST":
        selected_year = request.form.get("year_group", "")
        if selected_year in YEAR_GROUPS:
            session["year_group"] = selected_year
        return redirect(url_for("elective"))

    year_group = session.get("year_group")
    if not year_group:
        return redirect(url_for("userform"))

    subjects = ELECTIVE.get(year_group, [])

    if year_group == "Others":
        elective_files = {}
        for year, year_data in ELECTIVE_FILES.items():
            if year == "Others":
                continue
            for subject, files in year_data.items():
                elective_files.setdefault(subject, [])
                for f in files:
                    item = {"title": f"[Year {year}] {f['title']}"}
                    if "url" in f:
                        item["url"] = f["url"]
                    else:
                        item["filename"] = f["filename"]
                    elective_files[subject].append(item)
    else:
        elective_files = ELECTIVE_FILES.get(year_group, {})

    return render_template(
        "elective.html",
        year_group=year_group,
        year_groups=YEAR_GROUPS,
        subjects=subjects,
        elective_files=elective_files,
    )


@app.route("/subject")
def subject():
    return render_template("subject.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
