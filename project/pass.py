from flask import Flask,render_template,request
from cryptography.fernet import Fernet
import MySQLdb
import details
app = Flask(__name__)

@app.route('/add',methods =["POST","GET"])
def add():
	pwd = request.form.get('password')
	usr = request.form.get('username')
	key = details.details.key
	cipher_suite = Fernet(key)
	ciphered_text = cipher_suite.encrypt(pwd.encode())
	con = MySQLdb.connect("localhost","root","","test")	
	cursor = con.cursor()  #required to be bytes
	cursor.execute("INSERT INTO `encrypt` VALUES ('"+usr+"', %s)",(ciphered_text,))
	con.commit()
	return("<br><br><br><br><br><center>successful</center>")

@app.route('/',methods =["GET"])
def new():
	return(render_template('pass.html'))



if __name__ == '__main__':
	app.run(debug=True)