from flask import render_template,request,redirect,url_for,session
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'

@webapp.route('/login',methods=['GET'])
def login():
    return render_template("login/login.html")

@webapp.route('/login/check',methods=['POST'])
def login_check():
    table = dynamodb.Table('Users')

    account = request.form.get('account')
    password = request.form.get('password')

    response = table.query(
        KeyConditionExpression=Key('email').eq(account)
    )

    if len(response['Items']) == 0:
        return render_template("login/login.html",error="Account doesn't exist!")
    elif response['Items'][0]['password'] != password:
        return render_template("login/login.html", error="Password is wrong!")

    session['account'] = account
    session['password'] = password

    return redirect(url_for("self_view"))
