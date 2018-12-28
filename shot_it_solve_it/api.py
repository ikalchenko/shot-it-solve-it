from flask import Flask, jsonify, request
from shot_it_solve_it.model import predict_numbers
from os import path

app = Flask(__name__)
UPLOAD_FOLDER = '/home/ikalchenko/education/shot-it-solve-it/media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def main():
    return jsonify({'info': 'Shot it! Solve it! API'})

@app.route('/predict', methods=['POST'])
def predict():
    img = request.files['file']
    img.save(path.join(UPLOAD_FOLDER, img.filename))
    result = predict_numbers(path.join(UPLOAD_FOLDER, img.filename))
    return jsonify({'info': result})


if __name__ == '__main__':
    app.run(debug=False)
