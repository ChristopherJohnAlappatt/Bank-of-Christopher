from flask import Flask, flash,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

import MySQLdb.cursors

app = Flask(__name__)


app.secret_key = 'TIGER'

app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6400231'
app.config['MYSQL_PASSWORD'] = 'wlByAskHda'
app.config['MYSQL_DB'] = 'sql6400231'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('index.html')

# @app.route("/customerpage")
# def customer():
#     return render_template('customerpage.html')

@app.route("/customer")
def cust():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM CUSTOMERS")
    customerdata=cursor.fetchall()
    print(customerdata)
    return render_template('customerpage.html', data=customerdata)


# @app.route("/profile", methods=['GET', 'POST'])
# def prof():
#     if request.method == 'POST' and 'cname' in request.form:
#         user=request.form['cname']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("SELECT id FROM customers WHERE name=%s",(user,))
#         pid=cursor.fetchall()
#         print(user)
#     return render_template('profile.html',value=pid)

@app.route('/profile', methods =['GET','POST'])
def prof():
    if request.method=='POST' and 'cid' in request.form :
        #cursor = mysql.connection.cursor()
        sender_id=request.form['cid']
        sender_name=request.form['cname']
        sender_email=request.form['cemail']
        sender_balance=request.form['cbal']
        print(sender_id,sender_name,sender_email,sender_balance)
        print('cname')
        print('cemail')
        print('cbal')
        return(render_template("profile1.html",username=sender_name,userid=sender_id,useremail=sender_email,userbalance=sender_balance))

@app.route('/transaction', methods =['GET','POST'])
def transaction():
    if request.method=='POST' and 'reciever_username' in request.form :
        print("Im in if statement")
        reciever_username=request.form['reciever_username']
        ramount=float(request.form['ramount'])
        sender_name=(request.form['username'])
        sender_balance=float(request.form['userbalance'])
        # print(reciever_username)s
        # print(ramount)
        # print(sender_name)
        # print(sender_balance)
        sender_current_balance=sender_balance-ramount
        cursor=mysql.connection.cursor()
        cursor.execute('Select Balance from CUSTOMERS where Name =%s',(reciever_username,))
        reciever_balance=cursor.fetchone()
        reciever_balance=reciever_balance[0]
        print(reciever_balance)
        reciever_current_balance=ramount+reciever_balance
        
        if sender_current_balance>0:
            cursor=mysql.connection.cursor()
            cursor.execute('Update CUSTOMERS SET Balance=%s Where Name=%s',(sender_current_balance,sender_name))
            cursor.execute('Update CUSTOMERS SET Balance=%s Where Name=%s',(reciever_current_balance,reciever_username))
            cursor.execute("INSERT INTO transactions(sname,rname,amount) VALUES ( %s, %s,%s)", (sender_name, reciever_username, ramount,))
            mysql.connection.commit()
            return redirect(url_for("transaction2")) 
        else:
            return("Insufficient Balance")
        
    else:
        flash('THE USERNAME IS NOT REGISTERED IN THE DATA BASE . PLEASE TRY AGAIN','danger')
        # flash('You were successfully logged in')
        return redirect(url_for('home')) 

@app.route('/transaction2',methods=['GET', 'POST'])
def transaction2():
    cursor=mysql.connection.cursor()
    cursor.execute("Select * from transactions order by time desc")
    my_list=cursor.fetchall()
    mysql.connection.commit()
    return(render_template("transaction.html",list=my_list))

    return ("Hello World")
if __name__=="__main__":
    app.run(debug=True)
