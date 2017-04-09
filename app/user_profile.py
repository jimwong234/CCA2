from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@webapp.route('/profile',methods=['GET'])
def profile():
    username = session['username']
    profile_img = session['profile_img']
    email = session['account']
    table = dynamodb.Table('Users')
    r = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    data = {}
    data['email'] = r['Items'][0]['email']
    data['about_me'] = r['Items'][0]['about_me']
    data['age'] = r['Items'][0]['age']
    data['gender'] = r['Items'][0]['gender']
    data['location'] = r['Items'][0]['location']
    data['occupation'] = r['Items'][0]['occupation']
    data['phone'] = r['Items'][0]['phone']
    data['username'] = r['Items'][0]['username']

    userimg = r['Items'][0]['profileimg']
    if userimg == 'null':
        userimg = 'static/images/DefaultProfilePic.jpg'
    else:
        userimg = "https://s3.amazonaws.com/mcc123/" + userimg

    data['profileimg'] = userimg
    return render_template("userUI/profile.html", profileimg=profile_img, username=username,data=data,flag="profile")
