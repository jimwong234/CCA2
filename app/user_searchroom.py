from flask import render_template,session,request,redirect,url_for
from app import webapp
from boto3.dynamodb.conditions import Key, Attr

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@webapp.route('/searchroom',methods=['GET'])
def searchroom():
    username = session['username']
    profile_img = session['profile_img']
    return render_template("userUI/searchroom.html",profileimg=profile_img,username=username)

@webapp.route('/search',methods=['POST'])
def search():
    selfusername = session['username']
    profile_img = session['profile_img']

    usertable = dynamodb.Table('Users')
    posttable = dynamodb.Table('Posts')

    location = request.form.get('location')
    roomtype = request.form.get('room_type')

    if request.form.get('min_price'): #
        pricelower = int(request.form.get('min_price'))
    else:
        pricelower = 0
    if request.form.get('max_price'): #
        priceupper = int(request.form.get('max_price'))
    else:
        priceupper = 10000000
    if request.form.get('rent_months'):
        rent_months = int(request.form.get('rent_months'))
    else:
        rent_months = 0

    start_date_from = request.form.get('start_date_from')
    start_date_to = request.form.get('start_date_to')

    pe = "post_time, email, roomtype, price, #loc, start_date, rent_months"
    ean = {"#loc": "location", }
    response = posttable.scan(
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean,
        FilterExpression=Attr('location').eq(location) & Attr('roomtype').eq(roomtype) & Attr('price').between(
            pricelower, priceupper) & Attr('rent_months').gte(rent_months) & Attr('start_date').gte(start_date_from) &
            Attr('start_date').lte(start_date_to)
        # is_in or contains
    )

    records = []

    for i in response['Items']:
        email = i['email']
        r = usertable.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        username = r['Items'][0]['username']
        userimg = r['Items'][0]['profileimg']
        if userimg == 'null':
            userimg = 'static/images/DefaultProfilePic.jpg'
        else:
            userimg = "https://s3.amazonaws.com/mcc123/" + userimg
        i['username'] = username
        i['userimg'] = userimg
        records.append(i)

    return render_template("userUI/searchroom_results.html",records=records,profileimg=profile_img,username=selfusername)

@webapp.route('/get_issuer_info',methods=['POST'])
def get_issuer_info():
    username = session['username']
    profile_img = session['profile_img']
    email = session['account']

    issuer_email = request.form.get("email")
    table = dynamodb.Table('Users')
    r = table.query(
        KeyConditionExpression=Key('email').eq(issuer_email)
    )
    data = {}
    data['email'] = issuer_email
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

    #search friends db to see if both are friends
    table = dynamodb.Table('Friends')
    response = table.query(
            KeyConditionExpression=Key('email').eq(email) & Key('friend_email').eq(issuer_email)
    )
    print(response)
    if len(response['Items']) != 0:
        request_status = response['Items'][0]['adding_status'] #pending or friend
    else:
        response = table.query(
            KeyConditionExpression=Key('email').eq(issuer_email) & Key('friend_email').eq(email)
        )
        if len(response['Items']) != 0:
            request_status = response['Items'][0]['adding_status'] #pending or friend
        else:
            request_status = 2 #no pending and not friend

    data['request_status'] = request_status
    return render_template("userUI/profile.html", profileimg=profile_img, username=username, data=data, account=email)
