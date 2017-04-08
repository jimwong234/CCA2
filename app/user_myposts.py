from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@webapp.route('/myposts',methods=['GET'])
def myposts():
    username = session['username']
    profile_img = session['profile_img']
    email = session['account']
    table = dynamodb.Table('Posts')
    pe = 'post_time, #loc, roomtype, address'
    ean = {"#loc": "location"}
    response = table.scan(
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean,
        FilterExpression=Attr('email').eq(email)
    )
    records = []
    for i in response['Items']:
        records.append(i)
    return render_template("userUI/myposts.html", profileimg=profile_img, username=username,records=records,email=email)

@webapp.route('/post_details',methods=['POST'])
def post_details():
    email = session['account']
    username = session['username']
    profile_img = session['profile_img']

    post_user_email = request.form.get("post_user_email")
    post_time = request.form.get("post_time")
    flag = request.form.get("flag")

    table = dynamodb.Table('Posts')
    pe = '#loc, roomtype, start_date, rent_months, price, address, description, image'
    ean = {"#loc": "location"}
    response = table.get_item(
        Key={
            'email': post_user_email,
            'post_time': post_time
        },
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
    )

    data = {}
    if 'Item' in response:
        item = response['Item']
        image_string = item['image']
        image_list = image_string.split(',')
        item['image'] = image_list
        data.update(item)

    return render_template("userUI/post_details.html", profileimg=profile_img, username=username,data=data,flag=flag)

@webapp.route('/delete_post',methods=['POST'])
def delete_post():
    post_time = request.form.get("post_time")
    email = session['account']

    table = dynamodb.Table('Posts')

    table.delete_item(
        Key={
            'email': email,
            'post_time': post_time
        }
    )

    return redirect(url_for('myposts'))