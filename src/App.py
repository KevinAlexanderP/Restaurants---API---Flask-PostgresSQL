from flask import Flask , render_template , flash , redirect, url_for
from flask import request
from flask_mysqldb import MySQL 



## mysql Connection 
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskrestaurants'
mysql =MySQL(app)

## settings 
app.secret_key='mysecretkey'

@app.route('/')
def Index(): 
  cur=  mysql.connection.cursor()
  cur.execute('SELECT * FROM restaurants')
  data= cur.fetchall()
  # print(data)

  return render_template('index.html', restaurants= data)

@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
  if request.method == "POST": 
    id = request.form['id']
    rating= request.form['rating']
    name = request.form['name']
    site = request.form['site']
    email = request.form['email']
    phone = request.form['phone']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state'] 
    lat = request.form['lat']
    lng= request.form['lng']
    cur= mysql.connection.cursor()
    cur.execute('INSERT INTO restaurants (id,rating,name,site,email,phone,street, city, state, lat,lng) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
    (id,rating,name,site,email,phone,street, city, state, lat,lng))
    mysql.connection.commit()
    flash('restaurant added succesfully')

    return redirect(url_for('Index'))

@app.route('/update_restaurant/<string:id>' , methods = ['POST'])
def update_restaurant(id):
  if request.method == "POST": 
    rating= request.form['rating']
    name = request.form['name']
    site = request.form['site']
    email = request.form['email']
    phone = request.form['phone']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state'] 
    lat = request.form['lat']
    lng= request.form['lng']
    cur= mysql.connection.cursor()
    cur.execute("""
    UPDATE restaurants 
    SET 
    rating=%s ,
    name=%s ,
    site=%s ,
    email=%s ,
    phone=%s ,
    street=%s ,
    city=%s ,
    state=%s , lat=%s ,lng=%s 
    WHERE id=%s 
    """,(rating,name,site,email,phone,street, city, state, lat,lng,id))
    mysql.connection.commit()
    flash('restaurant added succesfully')
    return redirect(url_for('Index'))

@app.route('/edit/<id>' , methods = ['POST', 'GET'])
def get_restaurant(id ):
  cur=   mysql.connection.cursor()
  cur.execute('SELECT * FROM restaurants WHERE id= {0}'.format(id))
  data = cur.fetchall()
  cur.close()
  # print(data)
  # print(id)
  return render_template('edit-restaurant.html',restaurant = data[0])



# @app.route('/update/<string:id>', methods=['POST','GET'])
# def update_restaurant(id):
#   if request.method == 'POST':
#     id= request.form['id']
#     rating= request.form['rating']
#     name = request.form['name']
#     site = request.form['site']
#     email = request.form['email']
#     phone = request.form['phone']
#     street = request.form['street']
#     city = request.form['city']
#     state = request.form['state'] 
#     lat = request.form['lat']
#     lng= request.form['lng']  
#     cur= mysql.connection.cursor()
#     cur.execute('SELECT * FROM restaurants WHERE id= {0}'.format(id))
#     flash('restaurant updated succesfully')
#     return redirect(url_for('Index'))
#     print(id)
    



@app.route('/delete/<string:id>')
def delete_restaurant(id):
    cur=   mysql.connection.cursor()
    cur.execute('DELETE FROM restaurants where id= {0} '.format(id))
    mysql.connection.commit()
    flash('removed contact ')
    return redirect(url_for('Index'))


if __name__  == "__main__":
    app.run(port = 3000 ,debug= True)