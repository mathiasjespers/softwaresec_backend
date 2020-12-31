from flask import Flask, request, jsonify, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins="*")

def getScore(user):
    # TODO : get user highscore from sql database
    highscore = True
    return highscore;

def postScore(user, score):
    # TODO : send user & score to sql database
    return True

# flask get score route
@app.route('/score', methods=['GET'])
def get():
    user = request.json['user']
    getScore(user)
    return jsonify({'highscore': ''})


# flask post highscore route
@app.route('/score', methods=['POST'])
def post():
    score = request.json['score']
    user = request.json['user']
    postScore(user, score)
    return jsonify({})


if __name__ == '__main__':
    app.run()
