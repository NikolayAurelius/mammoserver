from flask import Flask, request, redirect, flash, url_for, jsonify, send_file
from models import model_1, model_2, model_3, model_4, bad, stranger
import os
from datetime import datetime
import numpy as np
from mammo_packets import read_from_file_binary, parse_mammograph_raw_data, parse_uncompressed_mammograph_packets
from amplitude import meas_to_x

import requests, io

WORKDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = f'{WORKDIR}/uploads'
ALLOWED_EXTENSIONS = {'bin', 'biz'}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#models = [model_1, model_2, model_3, model_4]
app = Flask(__name__)

#plot_app_url = 'http://0.0.0.0:5002'
plot_app_url = 'http://127.0.0.1:5002'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': True, 'error_type': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            print(file.filename)
            extention = file.filename.rsplit('.', 1)[1].lower()
            filename = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.{extention}'
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            parser = parse_mammograph_raw_data

            # TODO: Из-за того, что утилита сохраняет всё под одним файлом можем работать только с одним воркером
            if extention == 'biz':
                parser = parse_uncompressed_mammograph_packets
                raise NotImplementedError()

            data = read_from_file_binary(path)
            arr = parser(data)
            x = meas_to_x(arr)

            result = {'bad': bad(x)}
            for model in models:
                result[model.name] = model(x)

            result['stranger'] = stranger(result['torch_model_3'])
            return jsonify({'error': False, 'result': result})
        else:
            return jsonify({'error': True})

    return f'''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    
    <h1>Models: {str([elem.name for elem in models])}</h1>
    '''
@app.route('/get_plots', methods=['GET', 'POST'])
def get_plots():
    if request.method == 'POST':
        file = request.files['file']
        if 'ask_plots' in request.headers:
            ans = requests.post(plot_app_url, headers = {'instruction':'postfile', 'filename':file.filename})
            num = int(str(ans)[11:-2])
            if ans.headers['message'] == 'Sent':
                print('send zip file')
                return send_file(io.BytesIO(ans.content), mimetype = 'zip'), num, {'message':ans.headers['message']}
            elif 'imgscolvo' in ans.headers:
                return jsonify('I am page'), num, {'message':ans.headers['message'], 'imgscolvo': str(len(os.listdir(MYIMGDIR)))}
            return jsonify('I am page'), num, {'message':ans.headers['message']}
        #file.seek(0)
        #print(file.readline())
        #requests.post('http://127.0.0.1:5002/', files = {'file': file}, headers = {'instruction':'getfile'})
    return jsonify('Page to get plots')

if __name__ == '__main__':
    app.run(debug = True)
