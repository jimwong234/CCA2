from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

import os
import shutil

@webapp.route('/self_view',methods=['GET'])
def self_view():
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

    return render_template("userUI/selfview.html",profileimg=profile_img,username=username)


@webapp.route('/profile_img_update',methods=['POST'])
def profile_img_update():
    #get uploaded img
    if 'fileUploaded' not in request.files:
        return "Missing uploaded file"
    img = request.files['fileUploaded']
    #pad user name to img name
    img_name = img.filename
    account = session['account']
    img_padding_name = account + '_' + img_name
    #store img name after padding into corresponding user item
    table = dynamodb.Table('Users')
    table.update_item(
        Key={
            'email': account,
        },
        UpdateExpression="set profileimg = :p",
        ExpressionAttributeValues={
            ':p': img_padding_name
        }

    )
    #store img (img name after padding) to s3
    #store to local first
    fname = os.path.join('app/temp_imgs', img_padding_name)
    img.save(fname)
    #upload to s3
    s3 = boto3.client('s3')
    s3.upload_file(fname, "mcc123", img_padding_name)
    # change the image to be public-read
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("mcc123")
    object = s3.Object("mcc123", img_padding_name)
    object.Acl().put(ACL="public-read")
    bucket.Acl().put(ACL="public-read")
    # delete local files
    shutil.rmtree('app/temp_imgs')
    os.makedirs("app/temp_imgs")

    return redirect(url_for('self_view'))

@webapp.route('/signout',methods=['GET'])
def signout():
    session['account'] = ''
    session['password'] = ''
    return redirect(url_for('main'))