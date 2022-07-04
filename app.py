from flask import Flask,render_template,request,make_response,redirect
import os
import sqlite3

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def signup():
	if(request.cookies.get('userId')):
		return render_template("index.html",username=request.cookies.get("userId"))
	if(request.method=='POST'):
		conn = sqlite3.connect('data.db')
		con = conn.cursor()
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		conn.execute(f"CREATE TABLE IF NOT EXISTS data ('sno' INTEGER NOT NULL UNIQUE,'username' TEXT NOT NULL UNIQUE,'email' TEXT NOT NULL UNIQUE ,'password' TEXT NOT NULL ,PRIMARY KEY('sno' AUTOINCREMENT))  ")
		check_user = conn.execute(f"SELECT * FROM data where username='{username}' or  email='{email}'  ")
		check_result = check_user.fetchone()
		if(check_result):
			con.close()
			return render_template('signup.html',already="Already have account . Please take anothor username ?")
		else:
			conn.execute(f"INSERT INTO data (username,email,password) VALUES('{username}','{email}','{password}') ")
			conn.commit()
			con.close()
			return render_template('login.html',create_account="Successfuly create account .")
	else:
		return render_template('signup.html')

@app.route('/login',methods=["GET",'POST'])
def login():
	if(request.cookies.get('userId')):
		return render_template("index.html",username=request.cookies.get("userId"))
	if(request.method=='POST'):
		conn = sqlite3.connect('data.db')
		con = conn.cursor()
		username = request.form['username']
		password = request.form['password']
		res = conn.execute(f"SELECT * FROM data where username='{username}' and password='{password}' ")
		result = res.fetchone()
		if(result):
			if not (os.path.exists(f"./static/data/{username}")):
				os.mkdir(f"./static/data/{username}")
				print("yes")
			con.close()
			res = make_response(render_template('index.html',username=username))
			res.set_cookie("userId",f"{username}")
			print(request.cookies.get("userId"))
			return res
		else:
			con.close()
			return render_template('login.html',username_validate="Invalid username or password ?")
	else:
		return render_template('login.html')

@app.route("/upload_files",methods=['GET',"POST"])
def upload_files():
	if(request.method=="POST"):
		file = request.files['file']
		file.save(f"./static/data/{request.cookies.get('userId')}/{file.filename}")
		return render_template('index.html')

@app.route('/files')
def files():
	res = os.listdir(f"./static/data/{request.cookies.get('userId')}")
	user = request.cookies.get('userId')
	return render_template('files.html',res=res,user=user)

@app.route("/delete/<user>/<img>")
def remove(user,img):
	os.remove(f"./static/data/{user}/{img}")
	return redirect('/files')

@app.route('/donload_files')
def download_files():


@app.route('/logout')
def logout():
	res = make_response(render_template('login.html'))
	res.delete_cookie("userId")
	return res

if(__name__=='__main__'):
	app.run(debug=True)
