from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)  # ✅ Use name, not name

basedir = os.path.abspath(os.path.dirname(__file__))  # ✅ Use file, not file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create database

# Create the database tables once, when the app starts
with app.app_context():
    db.create_all()
# Routes
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    quantity = request.form['quantity']
    new_item = Item(name=name, quantity=int(quantity))
    db.session.add(new_item)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':  # ✅ Must be name == 'main'
    app.run(debug=True)