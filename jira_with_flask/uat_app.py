import MySQLdb.cursors
from flask import Flask,render_template,request,url_for,session,redirect
from flask_mysqldb import MySQL
from datetime import *
import time as t
from jira import JIRA
import re

user = "zaydansari786@gmail.com"
apitoken= "ATATT3xFfGF0fJLn3BBV5KvLYHlsWOPPP6_9a2rGMjA2_5YHHXd8_KkvW1eX8FQSQOX5inISU4Mjvnwit1YkJyPCMHGozxDHDM2KEWqRlwRQ44kPZuTRzkHjTsxVEb__hg6Mxpr6qhXnwDhW_PiHIyrmNKfxual3RJoEZ0MiBCNI2AlgDNBNDGA=9454FB8A"

app = Flask(__name__)
app.config['MYSQL_HOST'] = '192.168.23.168'
app.config['MYSQL_USER'] = 'mysql_user'
app.config['MYSQL_PASSWORD'] = 'Test@123'
app.config['MYSQL_DB'] = 'alnafi'
mysql= MySQL(app)
app.secret_key = 'somethingsomething'

myhome="HOME PAGE!!!!!!!!!!!!!!!!!!!!!!!"
# @app.route("/login")		#http://127.0.0.1:5000
# def login():
# 	return render_template("login_page.html")
#
# @app.route('/login_check',methods=['POST','GET'])
# def login_check():
# 	if request.method == "POST":
# 		cursor = mysql.connection.cursor()
# 		username = request.form['username']
# 		password = request.form['password']
# 		sql = "select username,email,password from users;"
# 		cursor.execute(sql)
# 		result = cursor.fetchall()
# 		list_username = []
# 		list_password = []
# 		for i in result:
# 			if (username == i[0] or username == i[1]) and (password == i[2]):
# 				return render_template("trainer_form.html")
# 		else:
# 			return render_template('login_page.html')
@app.route('/login_page')
def login_page():
	return render_template('login.html')

@app.route('/login',methods=['POST','GET'] )
def login():
	msg=''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("select * from users where username = %s and password = %s",(username,password))
		account = cursor.fetchone()
		print(account)
		if account:
			session['loggedin']=True
			session['id']=account['id']
			session['username']=account['username']
			return render_template('index.html',username=session['username'])
		else:
			msg= "Incorrect Username/Password!!!"
			return render_template('login.html')
	return render_template('login.html',msg=msg)


@app.route('/logout')
def logout():
	session.pop('loggedin',None)
	session.pop('id',None)
	session.pop('username',None)
	return redirect(url_for('login_page'))

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/register',methods=['POST','GET'] )
def create_account():
	msg = ''
	msf = ''
	try:
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute("select * from users where username = % s ", (username,))
			account = cursor.fetchone()
			cursor.execute("select * from users where email = % s ", (email,))
			email_data = cursor.fetchone()
			if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Please enter valid email address'
				return render_template('register.html', msg=msg)
			elif account: #checks if any users already have the same username
				msg= 'User with same name already registered!!!'
				return render_template('register.html', msg=msg)
			elif email_data: #checks if any users already have the same email
				msg = 'User with same email already registered!!!'
				return render_template('register.html', msg=msg)
			elif username and password: #checks if username and password is not empty
				cursor.execute("INSERT INTO users VALUES(NULL,%s,%s,%s)", (username, password,email))
				mysql.connection.commit()
				# commit
				msg="Successfully registered!!!"
				msf = 'Login to continue'
				# close
				cursor.close()
		return render_template('login.html',msg=msg,msf=msf)
	except MySQLdb.ProgrammingError as e:
		msg=str(e)
		return render_template('register.html', msg=msg)
	finally:
		cursor.close()



@app.route("/")		#http://127.0.0.1:5000
def index():
	if 'loggedin' in session:
		return render_template("index.html",username=session['username'])
	return redirect(url_for('login_page'))

@app.route("/trainer")		#http://127.0.0.1:5000/contact
def trainer():
	if 'loggedin' in session:
		return render_template("trainer_form.html",username=session['username'])
	return redirect(url_for('login_page'))

@app.route("/trainer_create",methods=['POST','GET'])		#http://127.0.0.1:5000/contact
def trainer_create():
	if 'loggedin' in session:
		if request.method == "POST":
			fname_data= request.form['fname']
			lname_data = request.form['lname']
			design_data = request.form['design']
			course_data = request.form['course']
			cdate= date.today()
			sql = "INSERT INTO trainer_details (fname,lname,desig,course,datetime) VALUES (%s,%s,%s,%s,%s)"
			val = (fname_data,lname_data,design_data,course_data,cdate)

			#connection
			cursor = mysql.connection.cursor()

			#execute sql query
			cursor.execute(sql,val)

			#commit
			mysql.connection.commit()

			#close
			cursor.close()
			return render_template('trainer_form.html',username=session['username'])
		return redirect(url_for('login_page'))

@app.route("/trainer_data",methods=['POST','GET'])		#http://127.0.0.1:5000/contact
def trainer_data():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor()
		sql = "select * from trainer_details;"
		cursor.execute(sql)
		row =  cursor.fetchall()
		return render_template('trainer_report.html',output_data=row,username=session['username'])
	return redirect(url_for('login_page'))

@app.route("/trainer_filter",methods=['POST','GET'])		#http://127.0.0.1:5000/contact
def trainer_filter():
	if 'loggedin' in session:
		if request.method == "POST":
			course_search= request.form['course']
			cursor = mysql.connection.cursor()
			if course_search == "All":
				sql = "select * from trainer_details"
				cursor.execute(sql)
				row = cursor.fetchall()
				return render_template('trainer_report.html', output_data=row,username=session['username'])
			else:
				sql = "select * from trainer_details where course=" +course_search
				cursor.execute(sql)
				row = cursor.fetchall()
				return render_template('trainer_report.html', output_data=row,username=session['username'])
		return redirect(url_for('login_page'))

@app.route("/jira")
def jira():
	if 'loggedin' in session:
		return render_template("jira_page.html",username=session['username'])
	return redirect(url_for('login_page'))

@app.route("/jira_create",methods= ['POST','GET'])
def jira_create():
	if 'loggedin' in session:
		if request.method == "POST":
			project_data = request.form['project']
			issuetype_data = request.form['issuetype']
			reporter_data = request.form['reporter']
			summary_data = request.form['summary']
			desc_data = request.form['desc']
			priority_data = request.form['priority']
			assignee_data = request.form['assignee']
			server = "https://mzayd.atlassian.net"
			jira = JIRA(server,basic_auth=(user,apitoken))
			issue = jira.create_issue(project=project_data,summary=summary_data,description=desc_data,issuetype={'name':issuetype_data},priority={'name':priority_data},reporter={'id':reporter_data})
			issue.update(assignee={'accountId': assignee_data})
			print(issue)
			return render_template('jira_page.html',username=session['username'])
	return redirect(url_for('login_page'))


if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0")


