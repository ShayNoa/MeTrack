from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.exceptions import NotFound

from Tracker.config import bcrypt, create_app, db
from Tracker.forms import ExpenseForm, LoginForm, RegistrationForm
from Tracker.models import Category, Expense, User

def add_categories():
    categories = [
    'Education', 'Fitness', 'Groceries', 'Dining out', 'Transportation',
    'Utilities', 'Housing', 'Insurance', 'Kids', 'Medical', 
    'Clothing', 'Pets', 'Vacation', 'Personal', 'Entertainment', 'Other'] 
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()


app = create_app()

@app.errorhandler(NotFound)
def handle_bad_request(e):
    return render_template('404.html'), 400


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        User.create(form)
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_route = request.args.get('next')
            if next_route:
                return redirect(next_route)
            else:
                return redirect(url_for('profile'))        
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_expenses = User.get_expenses(current_user.id)
    category_expenses = Expense.by_categories(current_user.id)
    categories = [i[0] for i in category_expenses]
    sums = [i[1] for i in category_expenses]
    
    expenses_months =  Expense.by_months(current_user.id)
    months = [i[0] for i in expenses_months]
    amounts = [i[1] for i in expenses_months]
    
    form = ExpenseForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        Expense.create(form, current_user.id)
        flash(f'{form.name.data} added', 'success')
        return redirect(url_for('profile'))
    return render_template(
        'profile.html', 
        form=form, 
        category_expenses=category_expenses, 
        categories=categories, sums=sums, 
        months=months, 
        amounts=amounts, 
        user_expenses=user_expenses
        )


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id) 
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id): 
    expense = Expense.query.get_or_404(expense_id)
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

