from datetime import datetime

from flask_login import UserMixin

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
    
    expanses = db.relationship('Expense', backref='by_user', lazy=True) # lazy - effecs on loading the data. 

    def __repr__(self): 
        return f'{self.id}, {self.username}, {self.first_name}, {self.last_name}, {self.email}. {self.password}'
    

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False) 
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # ?? 
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self): 
        return f'{self.id}, {self.title}, {self.price}, {self.date}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String, nullable=False) 

    expenses = db.relationship('Expense', backref='expense', lazy=True)

    def __repr__(self): 
        return f'{self.name}'




def add_categories():
    categories = [
    'Education', 'Fitness', 'Groceries', 'Dining out', 'Transportation',
    'Utilities', 'Housing', 'Insurance', 'Kids', 'Self-Care', 'Health', 
    'Clothing', 'Pets', 'Vacation'] # how to add: Other?
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
