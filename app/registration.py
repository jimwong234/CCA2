from flask import render_template,request,redirect,url_for
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/registration',methods=['GET'])
def registration():
    return render_template("register/registration.html")

@webapp.route('/registration/submission',methods=['POST'])
def registration_submit():
    table = dynamodb.Table('Users')
    username = request.form.get('username')
    age = int(request.form.get('age'))
    gender = request.form.get('gender')
    email = request.form.get('email')
    phone = request.form.get('phone')
    occupation = request.form.get('occupation')
    password = request.form.get('password')
    confirm_password = request.form.get("cfpassword")  # confirm password
    about_me = request.form.get('about')
    location = ""
    locations = []
    if(request.form.get('downtown') == "downtown"):
        locations.append("downtown")
    if (request.form.get('northyork') == "northyork"):
        locations.append("northyork")
    if (request.form.get('markham') == "markham"):
        locations.append("markham")
    if (request.form.get('scarborough') == "scarborough"):
        locations.append("scarborough")
    if (request.form.get('mississauga') == "mississauga"):
        locations.append("mississauga")
    if (request.form.get('others') == "others"):
        locations.append("others")
    if len(locations) > 1:
        return render_template("register/registration.html",error="You can only choose one location!")
    elif len(locations) == 1:
        location = locations[0]
    if age > 120 or age < 5:
        return render_template("register/registration.html",error="Not a valid age")
    if password != confirm_password:
        return render_template("register/registration.html",error="Please enter the same password!")

    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    if len(response['Items']) > 0:
        return render_template("register/registration.html", error="Email already exists, please login or enter another email!")

    if occupation == "":
        occupation = "null"
    if about_me == "":
        about_me = "null"
    if location == "":
        location = "null"

    response = table.put_item(
        Item={
            'username':username,
            'age':age,
            'gender':gender,
            'email':email,
            'phone':phone,
            'occupation':occupation,
            'password':password,
            'about_me':about_me,
            'location':location,
            'profileimg':"null"
        }
    )

    return redirect(url_for('login',approved=1))