from flask import Flask, request, redirect, flash, url_for, render_template
from models import model, runModel
import time
import os
from datetime import datetime
import numpy as np
from PIL import Image
import pyheif

WORKDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = f'{WORKDIR}/static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'heic'}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return redirect(url_for('upload_file'))


@app.route('/melanoma', methods=['GET', 'POST'])
def upload_file():

    status = None
    showimg = None

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            status = 'Error: No file part'

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
            if (file.filename.rsplit('.', 1)[1].lower() == 'heic'):
                status = 'I cant do heic files yet'
                im = Image.open(file.stream)
                #im = pyheif.read(file.stream)
                #im = Image.frombytes(im.mode, im.size, im.data,"raw", im.mode, im.stride)
            else:
                im = Image.open(file.stream)
            im = im.convert('RGB')
            filename = filename + '.jpg'           
            showimg = filename
            diagns = runModel(im, model)
            im.save(os.path.join(UPLOAD_FOLDER,filename), "JPEG")
            result = diagns
            status = f'Your result: {str(int(round(100 * result[0][0])))}%'
        else:
            status = 'File should be .jpg, .jpeg or .png'

    return render_template('main_page.html', status = status, showimg = showimg)


if __name__ == '__main__':
    app.run(debug = True)
