from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask_login import current_user, login_required

from Tracker import db
from Tracker.expenses.forms import ExpenseForm
from Tracker.models import Category, Expense, User

expenses = Blueprint('expenses', __name__)


@expenses.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_expenses = User.get_expenses(current_user.id)
    category_expenses = User.expenses_by_category(current_user.id)
    categories = [expense[0] for expense in category_expenses]
    sums = [expense[1] for expense in category_expenses]
    
    expenses_months = User.expenses_by_months(current_user.id)
    months = [expense[0] for expense in expenses_months]
    amounts = [expense[1] for expense in expenses_months]

    form = ExpenseForm()
    if request.method == "POST" and form.validate_on_submit():
        Expense.create(form, current_user.id)
        flash(f"{form.name.data} added", "success")
        return redirect(url_for("expenses.profile"))
    return render_template(
        "profile.html",
        form=form,
        category_expenses=category_expenses,
        categories=categories,
        sums=sums,
        months=months,
        amounts=amounts,
        user_expenses=user_expenses,
    )


@expenses.route("/edit_expense/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        return redirect(url_for("expenses.profile")) # not tested

    form = ExpenseForm()
    if request.method == "POST" and form.validate_on_submit:
        category_id = Category.get_id_by_name(form.category.data)
        expense.name = form.name.data
        expense.cost = form.cost.data
        expense.category_id = category_id
        expense.date = form.date.data
        db.session.commit()
        flash(f"{form.name.data} changes saved", "success")
        return redirect(url_for("expenses.profile"))

    if request.method == "GET":
        edit_form = ExpenseForm(obj=expense)
        category = Category.query.get(expense.category_id)
        edit_form.category.data = category
        return render_template("edit.html", expense=expense, edit_form=edit_form)


@expenses.route("/delete_expense/<int:expense_id>") # WHY THIS IS GET>?
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()
        flash(f"{expense.name} has been deleted", "success")
    return redirect(url_for("expenses.profile"))