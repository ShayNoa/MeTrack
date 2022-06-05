from flask_login import UserMixin
from sqlalchemy.sql.functions import func

from Tracker import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    expenses = db.relationship("Expense", backref="by_user", lazy=True)

    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def __repr__(self): # not tested
        return f"""{self.id}, {self.username}, {self.first_name}, 
                {self.last_name}, {self.email}, {self.password}"""

    @classmethod
    def create(cls, f):
        user = cls(
            username=f.username.data,
            first_name=f.first_name.data,
            last_name=f.last_name.data,
            email=f.email.data,
            password=f.password.data
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def by_email(cls, user_email):
        return cls.query.filter_by(email=user_email).first()

    @classmethod
    def get_expenses(cls, current_user_id):
        return (
            db.session.query(Expense, Category.name)
            .join(cls, Category)
            .filter(cls.id == current_user_id)
            .order_by(Expense.date.desc())
            .all()
        )

    @classmethod
    def expenses_by_category(cls, user_id):
        return (
            db.session.query(Category.name, func.sum(Expense.cost))
            .join(cls, Category)
            .filter(cls.id == user_id)
            .group_by(Expense.category_id)
            .all()
        )

    @classmethod
    def expenses_by_months(cls, user_id):
        return (
            db.session.query(
                func.strftime("%Y-%m", Expense.date), func.sum(Expense.cost)
            )
            .join(cls)
            .filter(cls.id == user_id)
            .group_by(func.strftime("%Y-%m", Expense.date))
            .limit(6)
            .all()
        )


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self): # not tested
        return f"{self.id}, {self.name}, {self.cost}, {self.date}"

    @classmethod
    def create(cls, f, user_id):
        category_id = Category.get_id_by_name(f.category.data)
        expense = cls(
            name=f.name.data,
            cost=f.cost.data,
            date=f.date.data,
            user_id=user_id,
            category_id=category_id,
        )
        db.session.add(expense)
        db.session.commit()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    expenses = db.relationship("Expense", backref="expense", lazy=True)

    def __repr__(self):
        return f"{self.name}"

    @classmethod
    def get_id_by_name(cls, input_name):
        category = cls.query.filter_by(name=str(input_name)).first()
        return category.id


# used in order to add categoris to db
def add_categories():
    categories = [
        "Education", "Fitness", "Groceries", "Dining out", "Transportation",
        "Utilities", "Housing", "Insurance", "Kids", "Medical", "Clothing",
        "Pets", "Vacation", "Personal", "Entertainment", "Other"
    ]
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()
