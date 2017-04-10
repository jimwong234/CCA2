from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@webapp.route('/setting?errors=<string:errors>',methods=['GET'])
def setting(errors):
    username = session['username']
    profile_img = session['profile_img']
    email = session['account']

    #search user db to get old info of the user
    table = dynamodb.Table('Users')
    pe = 'age, phone, about_me'
    response = table.get_item(
        Key={
            'email': email
        },
        ProjectionExpression=pe
    )
    data = {}
    if 'Item' in response:
        item = response['Item']
        data.update(item)
    data['username'] = username

    return render_template("userUI/setting.html",profileimg=profile_img,username=username,data=data,errors=errors)

@webapp.route('/change_basic_info',methods=['POST'])
def change_basic_info():
    new_username = request.form.get('username')
    age = int(request.form.get('age'))
    phone = request.form.get('phone')
    about_me = request.form.get('about')

    if age > 120 or age < 5:
        errors = "Not a valid age!"
        return redirect(url_for("setting", errors=errors))

    if about_me == "":
        about_me = "null"

    table = dynamodb.Table('Users')
    table.update_item(
        Key={
            'email': session["account"],
        },
        UpdateExpression="set username = :un, age = :a, phone = :p, about_me = :ab",
        ExpressionAttributeValues={
            ':un': new_username,
            ':a':age,
            ':p':phone,
            ':ab':about_me
        }
    )
    session['username'] = new_username
    return redirect(url_for("setting", errors="Basic Info changed!"))

@webapp.route('/change_password', methods=['POST'])
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    cf_new_password = request.form.get('cf_new_password')

    #search old password with session['password']
    if old_password != session['password']:
        errors = "Please enter a right old password!"
        return redirect(url_for("setting",errors=errors))

    if new_password != cf_new_password:
        errors = "Please enter the same new password!"
        return redirect(url_for("setting", errors=errors))

    table = dynamodb.Table('Users')
    table.update_item(
        Key={
            'email': session["account"],
        },
        UpdateExpression="set password = :pd",
        ExpressionAttributeValues={
            ':pd': new_password
        }
    )
    session['password'] = new_password
    return redirect(url_for("setting", errors="Password changed!"))

@webapp.route('/change_profileimg', methods=['POST'])
def change_profileimg():
    img = request.files['profileimg']
    # pad user name to img name
    img_name = img.filename
    account = session['account']
    img_padding_name = account + '_' + img_name
    # store img name after padding into corresponding user item
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
    # store img (img name after padding) to s3
    # upload to s3
    s3 = boto3.client('s3')
    s3.upload_fileobj(img, "mcc123", img_padding_name)
    # change the image to be public-read
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("mcc123")
    object = s3.Object("mcc123", img_padding_name)
    object.Acl().put(ACL="public-read")
    bucket.Acl().put(ACL="public-read")

    session["profile_img"] = "https://s3.amazonaws.com/mcc123/" + img_padding_name
    return redirect(url_for("setting", errors="Profile Image changed!"))