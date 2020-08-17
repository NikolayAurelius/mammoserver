from flask import Flask, request, redirect, flash, url_for, render_template
from models import model, runModel
import os
from datetime import datetime
import numpy as np

WORKDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = f'{WORKDIR}/static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

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
            print(file.filename)
            filename = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg'
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            showimg = filename
            diagns = runModel(os.path.join(UPLOAD_FOLDER, filename), model)
            result = diagns
            status = f'Your result: {str(round(100 * result[0][0]))}%'
        else:
            status = 'File should be .jpg, .jpeg or .png'

    return render_template('main_page.html', status = status, showimg = showimg)


if __name__ == '__main__':
    app.run(debug = True)
