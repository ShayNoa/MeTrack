from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.sql.functions import func

from Tracker.config import bcrypt, create_app, db
from Tracker.forms import ExpenseForm, LoginForm, RegistrationForm
from Tracker.models import Category, Expense, User
from datetime import date


app = create_app()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=hashed_password)    
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_route = request.args.get('next')
            if next_route:
                return redirect(next_route)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    #import pdb;pdb.set_trace()
    user_expenses = User.get_expenses(current_user.id)
    category_expenses = Expense.by_categories(current_user.id)
    cat = [i[0] for i in category_expenses]
    sums = [i[1] for i in category_expenses]
    
    expenses_months =  Expense.by_months(current_user.id)
    months = [i[0] for i in expenses_months]
    amounts = [i[1] for i in expenses_months]
    
    form = ExpenseForm()
    form.category.query = Category.query.filter(Category.id > 0)
    
    if request.method == 'POST' and  form.validate_on_submit():
        category_id = Category.get_id_by_name(form.category.data)
        expense = Expense(
            name=form.name.data,
            cost=form.cost.data,
            date=form.date.data,
            user_id = current_user.id,
            category_id=category_id
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form, category_expenses=category_expenses, cat=cat, sums=sums, months=months, amounts=amounts, user_expenses=user_expenses)


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id) 
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id): 
    expense = Expense.query.get(expense_id)
    form = ExpenseForm() 
    if request.method == 'POST' and form.validate_on_submit:
        category_id = Category.get_id_by_name(form.category.data)
        expense.name = form.name.data
        expense.cost = form.cost.data
        expense.category_id = category_id
        expense.date = form.date.data
        db.session.commit()
        flash(f'{form.name.data} changes saved', 'success')
        return redirect(url_for('profile'))
    
    if request.method == 'GET':
        edit_form = ExpenseForm(obj=expense)
        category = Category.query.get(expense.category_id)
        edit_form.category.data = category    
        return render_template('edit.html', expense=expense, edit_form=edit_form)
