from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  # needed for session


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
        return redirect(url_for("userform"))

    return render_template("signup.html")


@app.route("/userform", methods=["GET", "POST"])
def userform():
    name = session.get("name", "User")
    if request.method == "POST":
        year_group = request.form.get("year_group", "")
        if not year_group:
            return render_template(
                "userform.html", name=name, error="Please select a year group."
            )
        session["year_group"] = year_group
        return redirect(url_for("userprivate"))

    return render_template("userform.html", name=name)


@app.route("/userprivate")
def userprivate():
    name = session.get("name", "User")
    year_group = session.get("year_group")
    return render_template("userprivarte.html", name=name, year_group=year_group)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
