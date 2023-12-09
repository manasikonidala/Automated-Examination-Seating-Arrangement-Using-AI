from flask import Flask, render_template, request,redirect,url_for,flash
import sqlite3

from i3 import *
#from templates.db_code import PGASDB
app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template('index.html')

def get_db_connection():
    conn = sqlite3.connect('University.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/inputs',methods=['GET','POST'])
def inputs():
    return render_template('inputs.html')

@app.route('/aboutus',methods=['GET','POST'])

def aboutus():
    return render_template('aboutus.html')

@app.route('/login/login_check/home/login',methods=['GET','POST'])

@app.route('/login_check', methods=['POST'])
def login_check():
    mail = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAIL, PASSWORD FROM UNIVERSITY  WHERE MAIL = ? and PASSWORD = ?", (mail, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Successful login, redirect to some other page
        return redirect(url_for('inputs'))
    else:
        # Incorrect credentials, redirect back to login
        return redirect(url_for('login'))

# Signup route
    

@app.route('/signup',methods=['GET','POST'])

def signup():
    return render_template("signup.html")


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    mail = request.form['email']
    #phone = request.form['phone']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NAME,MAIL,PASSWORD FROM UNIVERSITY WHERE MAIL = ?;",(mail,))
    existing_user = cursor.fetchone()
    if existing_user:
        # User already exists, redirect to login page
        conn.close()
        return redirect(url_for('login'))
    else:
        cursor.execute("INSERT INTO UNIVERSITY (name, mail,password) VALUES (?, ?, ?)", (name, mail,password))
        conn.commit()
        conn.close()
        # Successful registration, redirect to some other page
        return redirect(url_for('inputs'))

@app.route('/generate_seating', methods=['POST'])


def generate_seating():
    global department1,department2,classroom
    classroom = request.form['classroom']
    department1 = request.form['department1']
    department2 = request.form['department2']

    if not is_valid_input(classroom, department1, department2):
        error_message = "Please enter valid department IDs and a valid classroom."
        return redirect(url_for('show_input', error_message=error_message))

    return result_display()

    
def is_valid_input(classroom, department1, department2):
  

    connection = sqlite3.connect('University.db')
    cursor = connection.cursor()

    # Check if the classroom and both department IDs exist
    cursor.execute("""
        SELECT COUNT(*)
        FROM CLASSROOM
        JOIN DEPARTMENT ON CLASSROOM.DEPARTMENT_ID = DEPARTMENT.DEPARTMENT_ID
        WHERE CLASSROOM.CLASSROOM_ID = ? AND DEPARTMENT.DEPARTMENT_ID IN (?, ?);
    """, (classroom, department1, department2))
    
    count = cursor.fetchone()[0]

    connection.close()

    return count == 1

@app.route('/show_input')
def show_input():
    err= request.args.get('error_message', '')
    return render_template('inputs.html', error_message=err)
    

def result_display():
    '''sch = main(classroom,department1,department2)
    
    return render_template('result.html'schedule=sch)'''
    seating_data = main(classroom, department1, department2)
    print(seating_data)
    return render_template('result.html', schedule=seating_data)




if __name__=='__main__':
    app.run(debug=True)
    
