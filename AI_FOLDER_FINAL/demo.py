import sqlite3

connection = sqlite3.connect('Customer.db')
cursor = connection.cursor()

# cursor.execute("drop table CUSTOMER;")
# sql_cmd='''CREATE TABLE CUSTOMER(
#            NAME VARCHAR(15), 
#            MAIL VARCHAR(25) NOT NULL, 
#            PHONE NUMBER PRIMARY KEY, 
#            PASSWORD VARCHAR(8) NOT NULL);'''

# cursor.execute(sql_cmd)
# print("Table created successfully")

# # cursor.execute("DESC Customer")

# sql_cmd='''INSERT INTO CUSTOMER VALUES(
#            'admin','admin@gmail.com',
#            9999999990,'admin');'''

# cursor.execute(sql_cmd)
# print("admin record added succesfully")

# sql_cmd='''INSERT INTO CUSTOMER VALUES(
#            'Ram','ram@gmail.com',
#            9999999991,'ram001');'''

# cursor.execute(sql_cmd)
# print("customer record added succesfully")

# connection.commit()

sql_cmd='''SELECT NAME, MAIL, PHONE, PASSWORD FROM CUSTOMER;'''
cursor.execute(sql_cmd)
rows=cursor.fetchall()
print(rows)

connection.commit()
connection.close()

from flask import Flask, render_template, request
import sqlite3
#from templates.db_code import PGASDB
app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])

def login():
    return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])

def signup():
    return render_template("signup.html")

@app.route('/register', methods=['GET','POST'])
def register():
    msg=''
    if request.method == 'POST':
        name=str(request.form['name'])
        mail=str(request.form['email'])
        ph=str(request.form['phone'])
        pasw=str(request.form['password'])
        if len(name)<15:
            if len(mail)<25:
                if '@gmail.com'in mail:
                    if len(str(ph))>0:
                        if len(pasw)<8:
                            connection=sqlite3.connect('Customer.db')
                            cursor=connection.cursor()
                            cursor.execute("SELECT NAME,MAIL,PASSWORD FROM CUSTOMER WHERE MAIL = ?;",(mail,))
                            row=cursor.fetchall()
                            connection.commit()
                            if len(row)==0:
                                cursor.execute('''INSERT INTO CUSTOMER VALUES(?,?,?,?);''',(name,mail,ph,pasw))
                                connection.commit()
                                print("............")
                                print('--------------')
                                return render_template('index.html')
                            else:
                                msg='          user already found,please sign in!'
                        else:
                            msg='         password length should be within 8 characters!'
                    else:
                        msg='          enter a valid phone number!'
                else:
                    msg='         email id should contain @gmail.com!'
            else:
                msg='          email-id too long!'
        else:
            msg='         name is more than the limit of 14 letters!'
    print(msg)
    return render_template('index.html',msg=msg)





if __name__=='__main__':
    app.run(debug=True)
