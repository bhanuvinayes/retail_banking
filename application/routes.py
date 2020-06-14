from application import app, db
from flask import render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    password = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer)
    cname = db.Column(db.String(20))
    age = db.Column(db.Integer)
    address = db.Column(db.Integer)
    state = db.Column(db.String(20))
    city = db.Column(db.String(20))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['pass']
        user = Employees(uname = uname, password = password)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successfull', category='info')
        return redirect( url_for('login') )
    return render_template('registration.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect( url_for('home') )

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        emp = Employees.query.filter_by(uname=username).first()
        if emp == None:
            flash('Invalid Credentials. Check User Name and Password', category='error')
            return redirect( url_for('login') )
        elif username == emp.uname and password == emp.password:
            session['username'] = username
            return redirect( url_for('home') )
        else:
            flash('Invalid Credentials. Check User Name and Password', category="error")

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        flash('You are logged out. Please login again to continue')
        return redirect( url_for('login') )

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been successfully logged out.')
    return redirect( url_for('login') )

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            cname = request.form['cname']
            age = request.form['age']
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']

            customer = Customers(ssn_id=ssn_id, cname=cname, age=age, address=address, state=state, city=city)
            db.session.add(customer)
            db.session.commit()
            flash('Customer added successfully')
            return redirect( url_for('create_customer') )
    else:
        flash('You are logged out. Please login again to continue')
        return redirect( url_for('login') )

    return render_template('customerScreen.html')