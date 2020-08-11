from flask import Flask
from models import model_1, model_2, model_3, model_4

models = [model_1, model_2, model_3, model_4]
app = Flask(__name__)


@app.route('/')
def hello_world():
    return str([elem.name for elem in models])


if __name__ == '__main__':
    app.run()
