from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/restaurants'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a model for the restaurants table
class Restaurant(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    rating = db.Column(db.Float)
    name = db.Column(db.String(255))
    site = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    data = Restaurant.query.all()
    return render_template('index.html', restaurants=data)

@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
    if request.method == "POST":
        new_restaurant = Restaurant(
            id=request.form['id'],
            rating=request.form['rating'],
            name=request.form['name'],
            site=request.form['site'],
            email=request.form['email'],
            phone=request.form['phone'],
            street=request.form['street'],
            city=request.form['city'],
            state=request.form['state'],
            lat=request.form['lat'],
            lng=request.form['lng']
        )
        db.session.add(new_restaurant)
        db.session.commit()
        flash('Restaurant added successfully')
        return redirect(url_for('Index'))

@app.route('/update_restaurant/<string:id>', methods=['POST'])
def update_restaurant(id):
    if request.method == "POST":
        restaurant = Restaurant.query.get(id)
        restaurant.rating = request.form['rating']
        # Update other fields similarly...
        db.session.commit()
        flash('Restaurant updated successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    return render_template('edit-restaurant.html', restaurant=restaurant)

@app.route('/delete/<string:id>')
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    db.session.delete(restaurant)
    db.session.commit()
    flash('Restaurant removed successfully')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)
