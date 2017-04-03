from flask import render_template,request
from app import webapp

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/registration',methods=['GET'])
def registration():
    return render_template("register/registration.html")

@webapp.route('/registration/submission',methods=['POST'])
def registration_submit():

    username = request.form.get('username')
    age = request.form.get('age')
    gender = request.form.get('gender')
    email = request.form.get('email')
    phone = request.form.get('phone')
    occupation = request.form.get('occupation')
    password = request.form.get('password')
    confirm_password = request.form.get("confirm_password")  # confirm password
    about_me = request.form.get('about')
    location = 0
    locations = []
    if(request.form.get('downtown') == "1"):
        locations.append(1)
    if (request.form.get('northyork') == "2"):
        locations.append(2)
    if (request.form.get('markham') == "3"):
        locations.append(3)
    if (request.form.get('scarborough') == "4"):
        locations.append(4)
    if (request.form.get('mississauga') == "5"):
        locations.append(5)
    if (request.form.get('others') == "6"):
        locations.append(6)
    if len(locations) > 1:
        return render_template("register/registration.html",error="You can only choose one location!")
    elif len(locations) == 1:
        location = locations[0]

    




    return render_template("register/registration.html")