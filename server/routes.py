import sys
import os
import json
import controller
import numpy as np
from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES

# app = Flask(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'label_img'
configure_uploads(app, photos)

@app.route('/', methods = ['GET','POST'])
def login():
    """Template for home of webpage

       :rtype: home template on html
    """
    if request.method == 'POST':
        session['username'] = request.form['username']
        print(request.form['username'])
        print(request.form['password'])
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/image', methods = ['GET','POST'])
def image():
    return render_template('upload.html')

@app.route('/image/image_upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date = request.form['date']
        print(firstname)
        print(lastname)
        print(date)
        [classification, probabilities] = controller.labeling("label_img/" + filename)
        return classification

@app.route('/image_data', methods=['POST'])
def image_data():
    """Routing that will post the image data

       :rtype: the index of the image
    """

    if(request.is_json):
        content = request.get_json()
        print(content)
    index = controller.store_image(content)
    print(index)
    return json.dumps(index)


@app.route('/image/<image_index>', methods=['GET'])
def image_index(image_index):
    """Routing to get the image index???

       :param image_index: image of the index
       :rtype: the index image???
       Daniel pls help
    """

    return image_index

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
