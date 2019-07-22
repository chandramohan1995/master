from flask import Flask, jsonify, request,render_template,Flask, session, redirect, g, url_for,flash
from sklearn.externals import joblib
import pandas as pd
import os
import json
from cryptography.fernet import Fernet
import MySQLdb
import details
from sklearn.linear_model import LinearRegression
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        #print("heyyyyyyyyyyyyyyyyyy")
        session.pop('user', None)
        pwd = request.form.get('password')
        usr = request.form.get('user')
        con = MySQLdb.connect("localhost","root","","test") 
        query ="SELECT pass FROM `encrypt` WHERE username ='"+usr+"' "
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        con.commit()
        #print("got here")
        try:

        	if request.form.get('password') == cipher_suite.decrypt(res[0][0]).decode():
            	session['user'] = request.form.get('username')
            	return(redirect(url_for('protected')))  
        except Exception as e:
        	print("<html><br><br><br><br><br><h2>invalid password</h2></html")
        


    return(render_template('index2.html'))

@app.route('/protected', methods=['GET', 'POST'])
def protected():
    if 'user' in session:



        return(render_template('index.html'))

    return(redirect(url_for('index2')))

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return(session['user'])

    return('Not logged in!')

@app.route('/dropsession', methods=['GET', 'POST'])
def dropsession():
    session.pop('user', None)
    flash("you have logged out succesfully")

    return(redirect(url_for('index2')))


@app.route("/predict",methods=['POST','GET'])
def predict():
	if 'user' in session:
		if(request.method == 'POST' or request.method == 'GET'):
			try:
            	#data = request.get_json()
				interest_rate =float(request.args.get("text"))
				#print(data)

				#interest_rate = data["interest_rate"]
				lin_reg = joblib.load("./reg_model.pkl")
			except ValueError:
				return("<br><br><br><br><center><h2>we are not capable enough to predict Home price with just a word. <br> please provide interest_rate</h2></center>")
			result=lin_reg.predict([[interest_rate]]).tolist()[0]
			return("<br><br><br><br><center><i><h3><b>Predicted Home price for your given Interest rate is  {}  </b></h3><i></center>".format(result))
		else:
			return("<html><h3>gthoh</h3></html>")
	else:
		return(redirect(url_for('index2')))

@app.route("/retrain",methods =['POST'])
def retrain():

	try:

		if 'user' in session:
			int_rate = float(request.form.get("text2"))
			home_price = float(request.form.get("text3"))
			training_label = pd.DataFrame(joblib.load("./training_labels.pkl"))
			training_set = joblib.load("./training_data.pkl")
			df_training_set= pd.DataFrame(data ={"interest_rate":[int_rate]})
			df_training_label = pd.DataFrame(data ={"Median home price":[home_price]})
		    
			df_training_set1 = pd.concat([training_label,df_training_label],axis =0,ignore_index =True)
			#print(df_training_set1)
			df_training_label1 = pd.concat([training_set,df_training_set],axis =0,ignore_index =True)
			#print(df_training_label)
			lr = LinearRegression()
			model = lr.fit(df_training_label1,df_training_set1)
			joblib.dump(model,"reg_model.pkl")
			return("<br><br><br><br><center><h2><b>Model retrain successful</b></h2></center>")

		else:
			return(redirect(url_for('index2')))
	except ValueError:
		return("<br><br><br><br><center><h2>model is not that intelligent to train itself. <br> please provide Home price, interest_rate</h2></center>")


@app.route('/add',methods =["POST","GET"])
def add():
    pwd = request.form.get('pass')
    usr = request.form.get('username')
    ciphered_text = cipher_suite.encrypt(pwd.encode())
    con = MySQLdb.connect("localhost","root","","test") 
    cursor = con.cursor()  #required to be bytes
    cursor.execute("INSERT INTO `encrypt` VALUES ('"+usr+"', %s)",(ciphered_text,))
    con.commit()
    return(render_template('success.html'))

if __name__ == '__main__':
    key = details.details.key
    cipher_suite = Fernet(key)
    app.run(port="5001",debug=True)
