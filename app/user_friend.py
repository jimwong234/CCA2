from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key,Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/add_friend',methods=['POST'])
def add_friend():
    self_email = session['account']
    friend_email = request.form.get("friend_email")
    table = dynamodb.Table('Friends')
    table.put_item(
        Item={
            'email': self_email,
            'friend_email': friend_email,
            'adding_status': 0  # requesting
        }
    )

    username = session['username']
    profile_img = session['profile_img']
    table = dynamodb.Table('Users')
    r = table.query(
        KeyConditionExpression=Key('email').eq(friend_email)
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
        userimg = "https://s3.amazonaws.com/mc123/" + userimg

    data['profileimg'] = userimg
    data['request_status'] = 0 #change to request pending

    return render_template("userUI/profile.html", profileimg=profile_img, username=username, data=data)

@webapp.route('/list_friend_requests',methods=['GET'])
def list_friend_requests():
    friend_table = dynamodb.Table('Friends')
    user_table = dynamodb.Table('Users')
    email = session['account']
    pe = 'email'
    response = friend_table.scan(
        ProjectionExpression=pe,
        FilterExpression=Attr('friend_email').eq(email) & Attr('adding_status').eq(0)
    )
    friend_request_records = []
    for i in response['Items']:
        email = i['email']
        r = user_table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        username = r['Items'][0]['username']
        userimg = r['Items'][0]['profileimg']
        useremail = r['Items'][0]['email']
        if userimg == 'null':
            userimg = 'static/images/DefaultProfilePic.jpg'
        else:
            userimg = "https://s3.amazonaws.com/mcc123/" + userimg
        i['username'] = username
        i['image'] = userimg
        i['email'] = useremail
        friend_request_records.append(i)

    self_email = session['account']
    friend_table = dynamodb.Table('Friends')
    friend_records = []
    pe = 'email'
    response = friend_table.scan(
        ProjectionExpression=pe,
        FilterExpression=Attr('friend_email').eq(self_email) & Attr('adding_status').eq(1)
    )
    for i in response['Items']:
        email = i['email']
        r = user_table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        username = r['Items'][0]['username']
        userimg = r['Items'][0]['profileimg']
        useremail = r['Items'][0]['email']
        if userimg == 'null':
            userimg = 'static/images/DefaultProfilePic.jpg'
        else:
            userimg = "https://s3.amazonaws.com/mcc123/" + userimg
        i['username'] = username
        i['image'] = userimg
        i['email'] = useremail
        friend_records.append(i)

    pe = 'friend_email'
    response = friend_table.scan(
        ProjectionExpression=pe,
        FilterExpression=Attr('email').eq(self_email) & Attr('adding_status').eq(1)
    )
    for i in response['Items']:
        email = i['friend_email']
        r = user_table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        username = r['Items'][0]['username']
        userimg = r['Items'][0]['profileimg']
        useremail = r['Items'][0]['email']
        if userimg == 'null':
            userimg = 'static/images/DefaultProfilePic.jpg'
        else:
            userimg = "https://s3.amazonaws.com/mcc123/" + userimg
        i['username'] = username
        i['image'] = userimg
        i['email'] = useremail
        friend_records.append(i)

    username = session['username']
    profile_img = session['profile_img']
    return render_template("userUI/friend.html", friend_request_records=friend_request_records,friend_records=friend_records, profileimg=profile_img, username=username)


@webapp.route('/confirm_friend_request',methods=['POST'])
def confirm_friend_request():
    requesting_email = request.form.get("email")
    self_email = session['account']
    friend_table = dynamodb.Table('Friends')
    friend_table.update_item(
       Key={
            'email': requesting_email,
            'friend_email': self_email
        },
        UpdateExpression = "set adding_status = :s",
        ExpressionAttributeValues = {
           ':s': 1
        }
    )
    return redirect(url_for('list_friend_requests'))

@webapp.route('/delete_friend_request',methods=['POST'])
def delete_friend_request():
    requesting_email = request.form.get("email")
    self_email = session['account']
    friend_table = dynamodb.Table('Friends')
    friend_table.delete_item(
        Key={
            'email': requesting_email,
            'friend_email': self_email
        }
    )
    return redirect(url_for('list_friend_requests'))

@webapp.route('/remove_friend',methods=['POST'])
def remove_friend():
    friend_email = request.form.get("friend_email")
    self_email = session['account']

    friend_table = dynamodb.Table('Friends')
    response = friend_table.scan(
        ProjectionExpression='email',
        FilterExpression=Attr('email').eq(self_email) & Attr('friend_email').eq(friend_email) & Attr('adding_status').eq(1)
    )
    if len(response['Items']) != 0:
        friend_table.delete_item(
            Key={
                'email': self_email,
                'friend_email': friend_email
            }
        )
    else:
        friend_table.delete_item(
            Key={
                'email': friend_email,
                'friend_email': self_email
            }
        )
    return redirect(url_for('list_friend_requests'))




