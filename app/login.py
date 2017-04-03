from flask import render_template
from app import webapp

@webapp.route('/login',methods=['GET'])
def login():
    return render_template("login/login.html")


