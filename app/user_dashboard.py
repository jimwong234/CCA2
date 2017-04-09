from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@webapp.route('/dashboard',methods=['GET'])
def dashboard():
    #search db to get user's info based on primary key account(email)
    table = dynamodb.Table('Users')
    account = session['account']

    response = table.get_item(
        Key={
            'email': account
        },
        ProjectionExpression="username,profileimg",
    )

    data = {}
    if 'Item' in response:
        item = response['Item']
        data.update(item)

    if data['profileimg'] == 'null':
        profile_img = 'static/images/DefaultProfilePic.jpg'
    else:
        profile_img = "https://s3.amazonaws.com/mcc123/" + data['profileimg']
    username = data['username']

    session['username'] = username
    session['profile_img'] = profile_img

    return render_template("userUI/dashboard.html",profileimg=profile_img,username=username)

@webapp.route('/signout',methods=['GET'])
def signout():
    session['account'] = ''
    session['password'] = ''
    session['username'] = ''
    session['profile_img'] = ''
    return redirect(url_for('main'))


