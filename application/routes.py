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
    cust_msg = db.Column(db.String(30))
    cust_status = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.now)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer)
    acnt_type = db.Column(db.String(20))
    acnt_status = db.Column(db.String(20))
    bal = db.Column(db.Integer)
    acnt_msg =  db.Column(db.String(30))
    date = db.Column(db.DateTime, default=datetime.now)

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

        user = Employees(uname = uname, password = password)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successfull', category='info')
        return redirect( url_for('login') )
    return render_template('emp_registration.html')


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


@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            customer_id = request.form['customer_id']

            if ssn_id != "":
                customer = Customers.query.filter_by( ssn_id = ssn_id).first()
                if customer == None:
                    flash('No customer with that ssn_id exists')
                    return redirect( url_for('search_customer') )
                else:
                    flash('Following details found')
                    return render_template('customer_found.html', customer = customer)
            
            if customer_id != "":
                customer = Customers.query.filter_by( id = customer_id).first()
                if customer == None:
                    flash('No customer with that customer id exists')
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


@app.route('/customer_found')
def customer_found():
    if 'username' in session:
        return render_template('customer_found.html')
    else:
        return redirect( url_for('login') )


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
            if customer == None or str(customer.id) != customer_id or str(customer.ssn_id) != ssn_id or str(customer.cname) != customer_name or str(customer.age) != age or str(customer.address) != address:
                flash('No customer with that that details found. Please enter correct details')
                return redirect( url_for('delete_customer') )
            else:
                db.session.delete(customer)
                db.session.commit()
                flash('Successfully deleted customer')
                return redirect( url_for('delete_customer') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('delete_customer.html')


# TODO Complete view function
@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    return render_template('update_customer.html', customer = request.args.get('customer'))


# TODO Complete
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if 'username' in session:
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
            
            if account_type == 'Savings':
                if savings == False:
                    account = Account( cust_id = int(cust_id), acnt_type = account_type, acnt_status = 'Active', bal = int(deposit_amount), acnt_msg = 'Account Created' )
                    db.session.add(account)
                    db.session.commit()
                    flash('Savings Account Created')
                    return redirect( url_for('create_account') )

            if account_type == 'Current':
                if current == False:
                    account = Account( cust_id = int(cust_id), acnt_type = account_type, acnt_status = 'Active', bal = int(deposit_amount), acnt_msg = 'Account Created' )
                    db.session.add(account)
                    db.session.commit()
                    flash('Current Account Created')
                    return redirect( url_for('create_account') )
            
            if account_type == 'Savings':    
                flash('Savings Account already created for this customer')
                return redirect( url_for('create_account') )
            else:
                flash('Current Account already created for this customer')
                return redirect( url_for('create_account') )
        
    else:
        return redirect( url_for('login') )

    return render_template('create_account.html')


@app.route('/delete_all', methods=['GET', 'POST'])
def delete_all():
    if request.method == 'POST':
        db.session.query(Employees).delete()
        db.session.commit()
        db.session.query(Customers).delete()
        db.session.commit()
        db.session.query(Account).delete()
        db.session.commit()
        flash('Deleted all customers record')
        return render_template('delete_all.html')
    return render_template('delete_all.html')


@app.route('/update_search', methods=['GET', 'POST'])
def update_search():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            customer_id = request.form['customer_id']

            if ssn_id != "":
                customer = Customers.query.filter_by(ssn_id = ssn_id).first()
                if customer == None:
                    flash('No customer with that ssn_id exists')
                    return redirect( url_for('update_search') )
                else:
                    flash('Following details found')
                    return render_template('update_customer.html', customer = customer)
            
            if customer_id != "":
                customer = Customers.query.filter_by(id = customer_id).first()
                if customer == None:
                    flash('No customer with that customer id exists')
                    return redirect( url_for('update_search') )
                else:
                    flash('Following details found')
                    return redirect( url_for('update_customer', customer = customer))
            
            if ssn_id == "" and customer_id == "":
                flash('Enter either snn_id or customer id to search')
                return redirect( url_for('update_search') )

        # ssn_id = request.form['ssn_id']
        # customer_id = request.form['customer_id']
        # if customer_id == "":
        #     return render_template('update_search.html', ssn_id = ssn_id, customer_id = customer_id)
        # else:
        #      return redirect( url_for('login') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('update_search.html')


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


@app.route('/customer_status')
def customer_status():
    if 'username' in session:
        customers = Customers.query.all()

        if not customers:
            flash('There are customers')
            return redirect( url_for('cusomer_status') )
        
        else:
            return render_template( 'customer_status.html', customers = customers )
    
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for( 'login' ) )
    
    return render_template('customer_status.html')


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
    

@app.route('/withdraw')
def withdraw():
    if 'username' in session:
        if request.method == 'POST':
            acnt_id = request.form['acnt_id']
            cust_id = request.form['cust_id']
            acnt_type = request.form['acnt_type']
            amount = request.form['amount']

            return render_template('withdraw.html')
        
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for('login') )
    
    return render_template('withdraw.html')


@app.route('/transfer')
def transfer():
    if 'username' in session:
        if request.method == 'POST':
            cust_id = request.form['cust_id']
            src_acnt_type = request.form['src_acnt_type']
            tar_acnt_type = request.form['tar_acnt_type']
            amount = request.form['amount']

            return render_template('Transfer.html')
    
    else:
        flash('You are logged out. Please login again')
        return redirect( url_for('login') )
    
    return render_template('Transfer.html')