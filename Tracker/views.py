from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from Tracker.config import bcrypt, create_app, db
from Tracker.forms import ExpenseForm, LoginForm, RegistrationForm
from Tracker.models import Category, Expense, User

from sqlalchemy.sql.functions import func

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
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    category_expenses = db.session.query(
        Category.name, func.sum(Expense.cost)).join(User, Category
        ).filter(User.id == current_user.id).group_by(Expense.category_id).all()
    categories = [i[0] for i in category_expenses]
    sums = [i[1] for i in category_expenses]
    form = ExpenseForm()
    form.category.query = Category.query.filter(Category.id > 0)
    
    if request.method == 'POST' and  form.validate_on_submit():
        selected_category = Category.query.filter(
            Category.name.like(f'%{form.category.data}%')
            ).first()
        expense = Expense(
            name=form.name.data,
            cost=form.cost.data,
            date=form.date.data,
            user_id = current_user.id,
            category_id=selected_category.id
        )
        db.session.add(expense)
        db.session.commit()
        return render_template('profile.html', form=form, category_expenses=category_expenses)

    return render_template('profile.html', form=form, category_expenses=category_expenses, categories=categories, sums=sums)


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
        selected_category = Category.query.filter(
            Category.name.like(f'%{form.category.data}%')
            ).first()
        expense.name = form.name.data
        expense.cost = form.cost.data
        expense.category_id = selected_category.id
        expense.date = form.date.data
        db.session.commit()
        flash(f'{form.name.data} changes saved', 'success')
        return redirect(url_for('profile'))
    
    if request.method == 'GET':
        edit_form = ExpenseForm(obj=expense)
        category = Category.query.get(expense.category_id)
        edit_form.category.data = category    
        return render_template('edit.html', expense=expense, edit_form=edit_form)


# Expense.query.join(User).filter(User.id == current_user.id).all()
# db.session.query(func.sum(Expense.cost)).join(User).filter(User.id == current_user.id).group_by(Expense.category_id)
# db.session.query(Category.name, func.sum(Expense.cost)).join(User, Category).filter(User.id == current_user.id).group_by(Expense.category_id).all() - sum of user expenses
# group by the category name. how to chart js now? i have a list of tuples in the format (category_name, total_amount). like this - [('Groceries', 52.0), ('Housing', 1000.0)].
# do i need to make it a json? json.dumps(dict(....))