from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from Tracker.config import bcrypt, create_app, db
from Tracker.forms import ExpenseForm, LoginForm, RegistrationForm
from Tracker.models import Category, Expense, User

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
    form = ExpenseForm()
    form.category.query = Category.query.filter(Category.id > 1)
    if request.method == 'POST' and  form.validate_on_submit():
        selected_category = Category.query.filter(
            Category.name.like(f'%{form.category.data}%')
            ).first()
        expense = Expense(
            title=form.name.data,
            price=form.amount.data,
            date=form.date.data,
            user_id = current_user.id,
            category_id=selected_category.id
        )
        db.session.add(expense)
        db.session.commit()
        return render_template('profile.html', form=form)
    return render_template('profile.html', form=form)


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    import pdb;pdb.set_trace()
    expense = Expense.query.get_or_404(expense_id) #get_or_404?
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('profile'))

# @app.route('/edit_expense/<int:expense_id>')
# def edit_expense(expense_id):
