from flask import flash, render_template, request, redirect, url_for
from app import app
from extensions import db
from models import Expense
from sqlalchemy import func


@app.route("/")
def home():

    category_totals = (
        db.session.query(
            Expense.category,
            func.sum(Expense.amount)
        )
        .group_by(Expense.category)
        .all()
    )

    grand_total = (
        db.session.query(
            func.sum(Expense.amount)
        )
        .scalar()
    )

    if grand_total is None:
        grand_total = 0

    return render_template(
        "index.html",
        category_totals=category_totals,
        grand_total=grand_total
    )

@app.route("/category/<category>")
def category_expenses(category):

    expenses = (
        Expense.query
        .filter_by(category=category)
        .all()
    )

    total = sum(expense.amount for expense in expenses)

    return render_template(
        "category.html",
        category=category,
        expenses=expenses,
        total=total
    )

@app.route("/add", methods=["GET", "POST"])
@app.route("/add/<category>", methods=["GET", "POST"])
def add_expense(category=None):

    if request.method == "POST":
        
        # Get category from hidden field or URL parameter
        category = request.form.get("category") or category
        
        # If no category from hidden field and no URL category, 
        # try to get from the display field (for new categories)
        if not category:
            category = request.form.get("category_display")
        
        name = request.form.get("name")
        amount = request.form.get("amount")
        
        # Validate
        if not all([name, amount, category]):
            flash("All fields are required", "error")
            return render_template("add.html", category=category)
        
        try:
            expense = Expense(
                name=name,
                amount=float(amount),
                category=category
            )

            db.session.add(expense)
            db.session.commit()

            return redirect(
                url_for(
                    "category_expenses",
                    category=category
                )
            )
        except Exception as e:
            db.session.rollback()  # Rollback on error
            flash(f"Database error: {str(e)}", "error")
            return render_template("add.html", category=category)

    return render_template(
        "add.html",
        category=category
    )

@app.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):

    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for("home"))
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):

    expense = Expense.query.get_or_404(id)

    if request.method == "POST":

        expense.name = request.form["name"]
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]

        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "edit.html",
        expense=expense
    )