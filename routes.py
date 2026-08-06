from flask import render_template
from app import app


@app.route("/")
def home():
    return render_template(
        "index.html",
        title="Expense Tracker v2",
        username="Ian"
    )