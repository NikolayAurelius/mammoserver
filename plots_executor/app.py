from flask import Flask, request, jsonify, send_file
import os

import numpy as np

app = Flask(__name__)

BINSDIR = 'vizualizations/bins'
IMGSDIR = 'vizualizations/images'

@app.route('/', methods=['GET', 'POST'])
def download_vizualizations():
    if request.method == 'POST':
        if request.headers['instruction'] == 'getfile':
            file = request.files['file']
            filename = file.filename
            if not (filename in os.listdir(BINSDIR)):
                file.save(BINSDIR + f'/{filename}')
        else:
            filename = request.headers['filename']
            MYIMGDIR = IMGSDIR + f'/{filename}'
            if not (os.path.isfile(MYIMGDIR + f'/{filename[:-4]}.zip')):
                    if (os.path.isdir(MYIMGDIR)):
                        return jsonify('I am page for vizualization'), 205, {'message':'In process', 'imgscolvo': str(len(os.listdir(MYIMGDIR)))}
                    return jsonify('I am page for vizualization'), 200, {'message':'Wait'}
            print('Отправляю файлы')      
            return send_file(IMGSDIR + f'/{filename}' + f'/{filename[:-4]}.zip', mimetype = 'zip'), 206, {'message':'Sent'}

    return jsonify('I am page for vizualization')

import  subprocess
if __name__ == '__main__':
    app.run(debug = True, port='5002')
    subprocess.Popen(['python.exe','draw_plots.py'])
