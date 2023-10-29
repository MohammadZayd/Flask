password = 'Test@123'

from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from datetime import *
import time as t
import mysql.connector

app = Flask(__name__)
app.config['MYSQL_HOST'] = '192.168.23.168'
app.config['MYSQL_USER'] = 'mysql_user'
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = 'alnafi'
mysql = MySQL(app)

myhome = "HOME PAGE"


@app.route("/")
def get_home():
    return myhome


@app.route("/trainer")
def trainer():
    return render_template("trainer_details.html")


# FORM connection
@app.route("/trainer_create", methods=['POST', 'GET'])
def trainer_create():
    if request.method == "POST":
        fname_data = request.form['fname']
        lname_data = request.form['lname']
        desig_data = request.form['desig']
        course_data = request.form['course']
        cdate = date.today()
        sql = "INSERT INTO trainer_details(fname,lname,desig,course,datetime) VALUES(%s,%s,%s,%s,%s)"
        val = (fname_data, lname_data, desig_data, course_data, cdate)

        # connection
        cursor = mysql.connection.cursor()

        # execute sql query
        cursor.execute(sql, val)

        # commit
        mysql.connection.commit()

        # close
        cursor.close()

        return render_template('trainer_details.html')

@app.route("/trainer_data",methods=['POST','GET'])
def trainer_data():
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM trainer_details;"
    cursor.execute(sql)
    row = cursor.fetchall()

    return render_template('display_trainer.html',output_data=row)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
