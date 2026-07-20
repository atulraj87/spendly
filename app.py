from flask import Flask, render_template, request, redirect, url_for, session

from database.db import get_db, init_db, seed_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template("register.html",
                                   error="All fields are required.",
                                   name=name, email=email)

        if len(password) < 8:
            return render_template("register.html",
                                   error="Password must be at least 8 characters.",
                                   name=name, email=email)

        db = get_db()
        if db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
            db.close()
            return render_template("register.html",
                                   error="An account with that email already exists.",
                                   name=name, email=email)

        db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password)),
        )
        db.commit()
        db.close()
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            return render_template("login.html",
                                   error="Invalid email or password.",
                                   email=email)

        db   = get_db()
        user = db.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
        db.close()

        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html",
                                   error="Invalid email or password.",
                                   email=email)

        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db      = get_db()
    row     = db.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()
    db.close()

    if row is None:
        session.clear()
        return redirect(url_for("landing"))

    user = {
        "name": row["name"],
        "email": row["email"],
        "member_since": datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y"),
    }
    stats = {
        "total_spent": "₹5,575",
        "transactions": 8,
        "top_category": "Shopping",
    }
    transactions = [
        {"date": "18 May 2026", "description": "New sneakers",      "category": "Shopping",     "amount": "₹2,500"},
        {"date": "10 May 2026", "description": "Pharmacy purchase",  "category": "Health",       "amount": "₹800"},
        {"date": "05 May 2026", "description": "Electricity bill",   "category": "Bills",        "amount": "₹1,200"},
        {"date": "03 May 2026", "description": "Metro card recharge","category": "Transport",    "amount": "₹120"},
        {"date": "01 May 2026", "description": "Groceries at D-Mart","category": "Food",         "amount": "₹450"},
    ]
    categories = [
        {"name": "Shopping",     "amount": "₹2,500", "pct": 45},
        {"name": "Bills",        "amount": "₹1,200", "pct": 22},
        {"name": "Health",       "amount": "₹800",   "pct": 14},
        {"name": "Food",         "amount": "₹545",   "pct": 10},
        {"name": "Transport",    "amount": "₹120",   "pct": 2},
        {"name": "Other",        "amount": "₹60",    "pct": 1},
    ]
    return render_template("profile.html", user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
