from unittest import result
from flask import Flask
from flask import request 
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
import mysql.connector

Assignment6 = Flask(
    __name__,
    static_folder = "public",
    static_url_path = "/"
)

Assignment6.secret_key = "大正紅茶拿鐵微糖去冰"

website = mysql.connector.connect(
    host="localhost",
    user="viviweikuo",
    password="zxcvbnmM12*",
    database="website"
)

mycursor = website.cursor(buffered=True)

@Assignment6.route("/")
def index():
    return render_template("index.html")

@Assignment6.route("/signup", methods=["POST"])
def signup():

    member_new_name = request.form["name"]
    member_new_username = request.form["username"]
    member_new_password = request.form["password"]

    member_search = "SELECT username FROM member WHERE username = %s"
    mycursor.execute(member_search, (member_new_username,))
    search_result = mycursor.rowcount

    if (search_result == 1):
        return redirect(url_for("error", error_message = "此帳號已被註冊"))
    else:
        session["name"] =  member_new_name
        session["username"] = member_new_username
        session["password"] = member_new_password

        member_add = "INSERT INTO member(name, username, password) VALUES(%s, %s, %s)"
        value = (member_new_name, member_new_username, member_new_password)
        mycursor.execute(member_add, value)
        website.commit()
        return redirect("/")

@Assignment6.route("/signin", methods=["POST"])
def signin():

    member_username = request.form["username"]
    member_password = request.form["password"]

    member_search = "SELECT username FROM member WHERE username = %s AND password = %s"
    mycursor.execute(member_search, (member_username, member_password,))
    search_result = mycursor.rowcount

    if (search_result == 1):
        session["username"] = member_username
        session["password"] = member_password
        return redirect("/member")
    else:
        return redirect(url_for("error", error_message = "帳號或密碼輸入錯誤"))

@Assignment6.route("/member")
def member():
    if "username" in session:
        member_search = "SELECT * FROM member WHERE username = %s AND password = %s"
        mycursor.execute(member_search, (session["username"], session["password"],))
        member = mycursor.fetchone()
        
        return render_template("member.html", name = member[1])
    else:
        return redirect("/")

@Assignment6.route("/error")
def error():
    result = request.args.get("error_message")
    return render_template("error.html", error_message = result)

@Assignment6.route("/signout")
def signout():
    session.pop("name", None)
    session.pop("username", None)
    session.pop("password", None)
    return redirect("/")

@Assignment6.route("/message", methods=["POST"])
def message():
    member_message = request.form["message"]
    message_add = "INSERT INTO message(content) VALUES(%s)"
    value = member_message
    mycursor.execute(message_add, (value,))
    website.commit()

    message_data = "SELECT content FROM message ORDER BY time DESC"
    mycursor.execute(message_data)
    all_message = mycursor.fetchall()
    
    return render_template("member.html", message = all_message)

Assignment6.run(port=3000)