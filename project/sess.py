from flask import Flask, session, render_template, request, redirect, g, url_for
import os
from cryptography.fernet import Fernet
import MySQLdb
import details
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        print("heyyyyyyyyyyyyyyyyyy")
        session.pop('user', None)
        pwd = request.form.get('password')
        usr = request.form.get('user')
        con = MySQLdb.connect("localhost","root","","test") 
        query ="SELECT pass FROM `encrypt` WHERE username ='"+usr+"' "
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        con.commit()
        print("got here")
        if request.form.get('password') == cipher_suite.decrypt(res[0][0]).decode():
            session['user'] = request.form.get('username')
            return(redirect(url_for('protected')))

    return(render_template('index2.html'))

@app.route('/protected', methods=['GET', 'POST'])
def protected():
    if 'user' in session:

        return(render_template('index.html'))

    return(redirect(url_for('index2')))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return(session['user'])

    return('Not logged in!')

@app.route('/dropsession', methods=['GET', 'POST'])
def dropsession():
    session.pop('user', None)
    return('Dropped!')



@app.route('/add',methods =["POST","GET"])
def add():
    pwd = request.form.get('password')
    usr = request.form.get('username')
    ciphered_text = cipher_suite.encrypt(pwd.encode())
    con = MySQLdb.connect("localhost","root","","test") 
    cursor = con.cursor()  #required to be bytes
    cursor.execute("INSERT INTO `encrypt` VALUES ('"+usr+"', %s)",(ciphered_text,))
    con.commit()
    return("<br><br><br><br><br><center>successful</center>")

if __name__ == '__main__':
    key = details.details.key
    cipher_suite = Fernet(key)
    app.run(port="5001",debug=True)
