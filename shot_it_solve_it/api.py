from flask import Flask, jsonify, request
from os import path

app = Flask(__name__)
UPLOAD_FOLDER = '/home/ikalchenko/education/shot-it-solve-it/media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def main():
    return jsonify({'info': 'Shot it! Solve it! API'})

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'info': 1})


if __name__ == '__main__':
    app.run(debug=False)
