"""
GET http://<your_server_address>:5000/analyse?text=<input_text>
"""
import flask
from flask import Flask, request
from analyse import get_fa, get_ta

app = Flask(__name__)

# request fa data
@app.route("/fa", methods=['GET','POS'])
def fa():
    if request.method == 'GET':
        ticker = request.args['text']
    elif request.method == 'POST':
        ticker = request.form['text']

    data = get_fa(ticker)
    return flask.jsonify(data)

# request ta data   
@app.route("/ta", methods=['GET','POS'])
def ta():
    if request.method == 'GET':
        ticker = request.args['text']
    elif request.method == 'POST':
        ticker = request.form['text']

    data = get_ta(ticker)
    return flask.jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)