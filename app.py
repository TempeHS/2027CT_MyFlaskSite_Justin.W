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
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "6": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "7": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "8": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "9": {
        "Mathematics": [
            {
                "title": "Year 9 Maths - Linear Relationships textbook",
                "filename": "files/core/9/mathematics/linear-notes.pdf",
            }
        ],
        "English": [
            {
                "title": "Year 9 English - The Monkey's Paw",
                "filename": "files/core/9/english/monkeyspaw.pdf",
            }
        ],
    },
    "10": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "11": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "12": {
        "Mathematics": [
            {
                "title": "Year 12 Maths - Calculus Notes",
                "filename": "files/core/12/mathematics/calculus-notes.pdf",
            }
        ]
    },
    "Others": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
}

ELECTIVE_FILES = {
    "5": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "6": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "7": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "8": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "9": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "10": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "11": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
    "12": {
        "Mathematics": [
            {
                "title": "Year 12 Maths - Calculus Notes",
                "filename": "files/core/12/mathematics/calculus-notes.pdf",
            }
        ]
    },
    "Others": {
        "Mathematics": [
            {
                "title": "Year 11 Maths - Algebra Notes",
                "filename": "files/core/11/mathematics/algebra-notes.pdf",
            }
        ]
    },
}


@app.route("/")
def home():
    return render_template("index.html")


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

    subjects = CORE.get(year_group, [])
    return render_template(
        "elective.html",
        year_group=year_group,
        year_groups=YEAR_GROUPS,
        subjects=subjects,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
