from flask_login import UserMixin
from sqlalchemy.sql.functions import func


from Tracker.config import db, login_manager


@login_manager.user_loader # read about it again.
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50)) 
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)  
    
    expenses = db.relationship('Expense', backref='by_user', lazy=True) # lazy - effecs on loading the data. 

    def __repr__(self): 
        return f'{self.id}, {self.username}, {self.first_name}, {self.last_name}, {self.email}, {self.password}'
    
    @classmethod
    def by_email(cls, user_email):
        return cls.query.filter_by(email=user_email).first()

    @classmethod
    def get_expenses(cls, current_user_id):
        return db.session.query(Expense, Category.name).join(
            cls, Category).filter(cls.id == current_user_id).order_by(
                Expense.date.desc()).all()
    

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False) 
    date = db.Column(db.Date, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self): 
        return f'{self.id}, {self.name}, {self.cost}, {self.date}'

    @classmethod
    def by_categories(cls, user_id):
        return db.session.query(Category.name, func.sum(cls.cost)).join(
                User, Category).filter(User.id == user_id).group_by(cls.category_id).all() 
    
    @classmethod
    def by_months(cls, user_id):
        return db.session.query(
            func.strftime('%Y-%m', cls.date), func.sum(cls.cost)).join(User).filter(
                User.id == user_id).group_by(func.strftime('%Y-%m', cls.date)).limit(6).all()
    

            

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String, nullable=False) 

    expenses = db.relationship('Expense', backref='expense', lazy=True)

    def __repr__(self): 
        return f'{self.name}'

    @classmethod
    def get_id_by_name(cls, input_name):
        category = cls.query.filter_by(name = str(input_name)).first()
        return category.id
        


def add_categories():
    categories = [
    'Education', 'Fitness', 'Groceries', 'Dining out', 'Transportation',
    'Utilities', 'Housing', 'Insurance', 'Kids', 'Self-Care', 'Health', 
    'Clothing', 'Pets', 'Vacation'] # how to add: Other?
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
