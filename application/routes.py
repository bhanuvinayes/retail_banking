from application import app, db
from flask import render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

# Creating Table for employees
class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    password = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

# Creating Table for customers
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer)
    cname = db.Column(db.String(20))
    age = db.Column(db.Integer)
    address = db.Column(db.Integer)
    state = db.Column(db.String(20))
    city = db.Column(db.String(20))
    cust_msg = db.Column(db.String(30))
    cust_status = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.now)


# Creating Table for accounts
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer)
    acnt_type = db.Column(db.String(20))
    acnt_status = db.Column(db.String(20))
    bal = db.Column(db.Integer)
    acnt_msg =  db.Column(db.String(30))
    date = db.Column(db.DateTime, default=datetime.now)

# Creating view function for registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        uname = request.form['uname']
        password = request.form['pass']
        cnfrm_password = request.form['cpass']

        query = Employees.query.filter_by(uname = uname).first()

        if query != None:
            if uname == str(query.uname):
                flash('Username already taken')
                return redirect( url_for('registration') )
        
        if password != cnfrm_password:
            flash('Password do not match')
            return redirect( url_for('registration') )

        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,20}$"
        pattern = re.compile(regex)

        match = re.search(pattern, password)
        
        if match:
            user = Employees(uname = uname, password = password)
            db.session.add(user)
            db.session.commit()
            flash('Registration was successfull', category='info')
            return redirect( url_for('login') )
        else:
            flash('Password should contain one Uppercase, one special character, one numeric character')
            return redirect( url_for('registration') )
    return render_template('emp_registration.html')


# Creating view function for login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:                # Checking for session login
        return redirect( url_for('home') )

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        emp = Employees.query.filter_by(uname=username).first()
        if emp == None:
            flash('Invalid Credentials. Check User Name and Password', category='error')
            return redirect( url_for('login') )
        elif username == emp.uname and password == emp.password:
            session['username'] = username  # saving session for login
            return redirect( url_for('home') )
        else:
            flash('Invalid Credentials. Check User Name and Password', category="error")

    return render_template('login.html')


# Creating view function for Home page
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        flash('You are logged out. Please login again to continue')
        return redirect( url_for('login') )

# Creating functionality for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been successfully logged out.')
    return redirect( url_for('login') )


# Creating view function for adding customer and writing relavent logic
@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if 'username' in session:                  # Checking session login
        if request.method == 'POST':           # Checkig for POST request
            ssn_id = request.form['ssn_id']
            cname = request.form['cname']      # retriving data from form of html page
            age = request.form['age']
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']

            # Quering racord from customer table
            cust = Customers.query.filter_by( ssn_id = ssn_id ).first()

            if cust == None:
                customer = Customers(ssn_id=ssn_id, cname=cname, age=age, address=address, state=state, city=city, cust_msg = 'Customer Created', cust_status = 'Active')
                db.session.add(customer)
                db.session.commit()
                flash('Customer added successfully')
                return redirect( url_for('create_customer') )
            
            else:
                flash('Customer with that SSN ID already exists')
                return redirect( url_for('create_customer') )
    else:
        flash('You are logged out. Please login again to continue')
        return redirect( url_for('login') )

    return render_template('create_customer.html')


# Creating view function for search customer and writing relavent logic for displaying customer details
@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            customer_id = request.form['customer_id']

            if ssn_id != "":
                customer = Customers.query.filter_by( ssn_id = ssn_id).first()
                if customer == None:
                    flash('No customer with that SSN ID exists')
                    return redirect( url_for('search_customer') )
                else:
                    flash('Following details found')
                    return render_template('customer_found.html', customer = customer)
            
            if customer_id != "":
                customer = Customers.query.filter_by( id = customer_id).first()
                if customer == None:
                    flash('No customer with that Customer ID exists')
                    return redirect( url_for('search_customer') )
                else:
                    flash('Following details found')
                    return render_template('customer_found.html', customer = customer)
            
            if ssn_id == "" and customer_id == "":
                flash('Enter either snn_id or customer id to search')
                return redirect( url_for('search_customer') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('search_customer.html')


# Function to display searched customer details
@app.route('/customer_found')
def customer_found():
    if 'username' in session:
        return render_template('customer_found.html')
    else:
        return redirect( url_for('login') )


# Function to delete customer record
@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            customer_id = request.form['customer_id']
            customer_name = request.form['customer_name']
            age = request.form['age']
            address = request.form['address']

            customer = Customers.query.filter_by(ssn_id = ssn_id).first()
            accounts = Account.query.filter_by( cust_id = customer_id ).all()
            if customer == None or str(customer.id) != customer_id or str(customer.ssn_id) != ssn_id or str(customer.cname) != customer_name or str(customer.age) != age or str(customer.address) != address:
                flash('No customer with that that details found. Please enter correct details')
                return redirect( url_for('delete_customer') )
            else:
                db.session.delete(customer)     # deleting customer
                db.session.commit()
                if not accounts:
                    flash('Successfully deleted customer')
                    return redirect( url_for('delete_customer') )
                
                for account in accounts:
                    db.session.delete(account)   # deleting accounts for customer
                    db.session.commit()
                flash('Successfully deleted customer')
                return redirect( url_for('delete_customer') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('delete_customer.html')


# View function for update customer
@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if 'username' in session:
        if request.method == 'POST':
            flash("Update function not written")
            return render_template('update_customer.html')
    else:
        flash('You have been logged out. Please login again')
        return redirect( url_for('login') )
    return render_template('update_customer.html')


# Function to create account for existing customers
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if 'username' in session:               # Checking for session login
        if request.method == 'POST':
            savings = False
            current = False

            cust_id = request.form['cust_id']
            account_type = request.form['account_type']
            deposit_amount = request.form['deposit_amount']

            customer_id = Customers.query.filter_by( id = cust_id ).first()
            
            if customer_id == None:
                flash('No customer exists with that id')
                return redirect( url_for('create_account') )
            
            # quring account details from accounts table
            acnt_cust_ids = Account.query.filter_by( cust_id = cust_id ).all()
            
            if not acnt_cust_ids:
                account = Account( cust_id = int(cust_id), acnt_type = account_type, acnt_status = 'Active', bal = int(deposit_amount), acnt_msg = 'Account Created' )
                db.session.add(account)
                db.session.commit()
                if account_type == 'Savings':
                    flash('Savings Account Created')
                    return redirect( url_for('create_account') )
                else:
                    flash('Current Account Created')
                    return redirect( url_for('create_account') )
            
            for acnt_cust_id in acnt_cust_ids:
                if acnt_cust_id.acnt_type == 'Savings':
                    savings = True
                if acnt_cust_id.acnt_type == 'Current': 
                    current = True
            
            # Creatind a savings account for existing customer
            if account_type == 'Savings':
                if savings == False:
                    account = Account( cust_id = int(cust_id), acnt_type = account_type, acnt_status = 'Active', bal = int(deposit_amount), acnt_msg = 'Account Created' )
                    db.session.add(account)
                    db.session.commit()
                    flash('Savings Account Created')
                    return redirect( url_for('create_account') )

            # Creating a current accoun for existing customer
            if account_type == 'Current':
                if current == False:
                    account = Account( cust_id = int(cust_id), acnt_type = account_type, acnt_status = 'Active', bal = int(deposit_amount), acnt_msg = 'Account Created' )
                    db.session.add(account)
                    db.session.commit()
                    flash('Current Account Created')
                    return redirect( url_for('create_account') )
            
            if account_type == 'Savings':    
                flash('Savings Account already created for this customer')     # Flashing relavent error message
                return redirect( url_for('create_account') )
            else:
                flash('Current Account already created for this customer')
                return redirect( url_for('create_account') )
        
    else:
        return redirect( url_for('login') )

    return render_template('create_account.html')

# Function to search for particular account
@app.route('/search_accounts', methods=['GET', 'POST'])
def search_accounts():
    if 'username' in session:
        if request.method == 'POST':
            account_id = request.form['account_id']
            customer_id = request.form['customer_id']

            if account_id != "":
                account = Account.query.filter_by( id = account_id).first()
                if account == None:
                    flash('No customer with that account ID exists')
                    return redirect( url_for('search_accounts') )
                else:
                    flash('Following details found')
                    return render_template('account_found.html', account = account)
            
            if customer_id != "":
                account = Account.query.filter_by( cust_id = customer_id).first()
                if account == None:
                    flash('No customer with that customer id exists')
                    return redirect( url_for('search_accounts') )
                else:
                    flash('Following details found')
                    return render_template('account_found.html', account = account)
            
            if account_id == "" and customer_id == "":
                flash('Enter either account id or customer id to search')
                return redirect( url_for('search_accounts') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('search_accounts.html')


# Function to display all existing account details
@app.route('/account_status')
def account_status():
    if 'username' in session:
        accounts = Account.query.all()

        if not accounts:
            flash('No accounts exists in database')
            return redirect( url_for('account_status') )
        else:
            return render_template('account_status.html', accounts = accounts)
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for('login') )

    return render_template('account_status.html')


# Function to delete account from database
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'username' in session:
        if request.method == 'POST':
            account_id = request.form['account_id']
            account_type = request.form['account_type']

            account = Account.query.filter_by( id = account_id ).first()

            if account == None:
                flash('No account with that account id exists')
                return redirect( url_for('delete_account') )
            
            if account.acnt_type == account_type:
                db.session.delete(account)
                db.session.commit()
                flash('Account deleted successfully')
                return redirect( url_for('delete_account') )
            else:
                if account_type == 'Current':
                    flash('Theres no Current Account for that customer')
                    return redirect( url_for('delete_account') )
                else:
                    flash('Thers no Savings Account for that customer')
                    return redirect( url_for('delete_account') )
        
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for('login') )

    return render_template('delete_account.html')

# Function for displaying all existing customer details
@app.route('/customer_status')
def customer_status():
    if 'username' in session:
        customers = Customers.query.all()

        if not customers:
            flash('There are customers')
            return redirect( url_for('customer_status') )
        
        else:
            return render_template( 'customer_status.html', customers = customers )
    
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for( 'login' ) )
    
    return render_template('customer_status.html')


# Function for depositing amount in particular account
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'username' in session:
        if request.method == 'POST':
            acnt_id = request.form['acnt_id']
            cust_id = request.form['cust_id']
            acnt_type = request.form['acnt_type']
            amount = request.form['amount']

            account = Account.query.filter_by( id = acnt_id ).first()

            if account == None:
                flash('No customer exists with that account id')
                return redirect( url_for('deposit') )
            
            if account.cust_id != int(cust_id):
                flash('Account ID and Customer ID do not match')
                return redirect( url_for('deposit') )
            
            if account.acnt_type != acnt_type:
                flash('Account ID and Account type do not match')
                return redirect( url_for('deposit') )
            
            account.bal = account.bal + int( amount )
            account.acnt_msg = 'Amount deposited'
            db.session.commit()

            flash('Amount deposited successfully')
            return redirect( url_for('deposit') )
        
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for('login') )
    
    return render_template('Deposit.html')
    
# Function to withdraw amount from particular account
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'username' in session:
        if request.method == 'POST':
            acnt_id = request.form['acnt_id']
            cust_id = request.form['cust_id']
            acnt_type = request.form['acnt_type']
            amount = request.form['amount']

            account = Account.query.filter_by( id = acnt_id ).first()

            if account == None:
                flash('No customer exists with that Account ID')
                return redirect( url_for('withdraw') )
            
            if account.cust_id != int(cust_id):
                flash('Account ID and Customer ID do not match')
                return redirect( url_for('withdraw') )
            
            if account.acnt_type != acnt_type:
                flash('Account ID and Account type do not match')
                return redirect( url_for('withdraw') )
            
            account.bal = account.bal - int( amount )
            account.acnt_msg = 'Amount Withdrawn'
            db.session.commit()

            flash('Amount withdrawn successfully')
            return redirect( url_for('withdraw') )
        
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for('login') )
    
    return render_template('withdraw.html')


# Function to transfer amount from either savings to current or current to savings
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' in session:
        if request.method == 'POST':
            cust_id = request.form['cust_id']
            src_acnt_type = request.form['src_acnt_type']
            tar_acnt_type = request.form['tar_acnt_type']
            amount = request.form['amount']
            accounts = 0
            
            if src_acnt_type == '' or tar_acnt_type == '':
                flash('Source account type and target account type can not be blank')
                return redirect( url_for('transfer') )
            
            if src_acnt_type == tar_acnt_type:
                flash('Source account type and Target Account Type can not be same')
                return redirect( url_for('transfer') )

            customers = Account.query.filter_by( cust_id = cust_id ).all()

            if not customers:
                flash('No customer exists with that Acccount ID')
                return redirect( url_for('transfer') )
            
            for customer in customers:
                accounts = accounts + 1
            
            if accounts == 1:
                flash('This customer has only one account')
            
            if accounts == 2:
                for customer in customers:
                    if customer.acnt_type == 'Savings':
                        savings_acnt = customer
                    if customer.acnt_type == 'Current':
                        current_acnt = customer
                
                if src_acnt_type == 'Savings':
                    savings_acnt.bal = savings_acnt.bal - int( amount )
                    savings_acnt.acnt_msg = 'Amount Transfered'
                    db.session.commit()
                    current_acnt.bal = current_acnt.bal + int( amount )
                    current_acnt.acnt_msg = 'Amount Transfered'
                    db.session.commit()
                    flash('Amount Transfered Successfully')
                    return redirect( url_for('transfer') )
                
                if src_acnt_type == 'Current':
                    savings_acnt.bal = savings_acnt.bal + int( amount )
                    savings_acnt.acnt_msg = 'Amount Transfered'
                    db.session.commit()
                    current_acnt.bal = current_acnt.bal - int( amount )
                    current_acnt.acnt_msg = 'Amount Transfered'
                    db.session.commit()
                    flash('Amount Transfered Successfully')
                    return redirect( url_for('transfer') )
    
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for('login') )
    
    return render_template('Transfer.html')


# Function to display account statements
@app.route('/account_statement', methods=['GET', 'POST'])
def account_statement():
    if 'username' in session:
        if request.method == 'POST':
            flash('Account statement function not written')
            return redirect( url_for('account_statement') )
        return render_template('account_statement.html')
    else:
        flash('You are logged. Please login again')
        return redirect( url_for('account_statement') )