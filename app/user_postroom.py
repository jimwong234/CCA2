from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

import os
import datetime
import shutil


@webapp.route('/postroom',methods=['GET'])
def postroom():
    username = session['username']
    profile_img = session['profile_img']
    return render_template("userUI/postroom.html",profileimg=profile_img,username=username)

@webapp.route('/new_post',methods=['POST'])
def new_post():
    table = dynamodb.Table('Posts')
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    email = session['account']
    post_time = '{:%Y-%m-%d-%H:%M:%S}'.format(datetime.datetime.now())
    location = request.form.get('location')
    roomtype = request.form.get('room_type')
    start_date = request.form.get('start_date')
    rent_months = int(request.form.get('rent_months'))
    price = int(request.form.get('price'))
    address = request.form.get('address')
    description = request.form.get('description')
    imagefile = request.files.getlist('imagefile')

    db_image_name = ''

    for f in imagefile:
        fn = f.filename
        s3_image_name = email + '__' + fn
        db_image_name = db_image_name + s3_image_name + ','
        fname = os.path.join('app/temp_imgs', s3_image_name)
        f.save(fname)
        s3_client.upload_file(fname, "mcc123", s3_image_name)
        bucket = s3_resource.Bucket("mcc123")
        object = s3_resource.Object("mcc123", s3_image_name)
        object.Acl().put(ACL="public-read")
        bucket.Acl().put(ACL="public-read")

    # delete local files
    shutil.rmtree('app/temp_imgs')
    os.makedirs("app/temp_imgs")

    db_image_name = db_image_name[:-1]

    if db_image_name == email + "__":
        db_image_name = "null"

    if description == "":
        description = "null"

    table.put_item(
        Item={
            'email': email,
            'post_time': post_time,
            'location': location,
            'roomtype': roomtype,
            'start_date': start_date,
            'rent_months': rent_months,
            'price': price,
            'address': address,
            'description': description,
            'image': db_image_name
        }
    )

    return redirect(url_for("postroom"))