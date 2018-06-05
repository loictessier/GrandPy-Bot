from flask import Flask, render_template, jsonify, request
from .grandpy import Grandpy

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/grandpy', methods=['POST'])
def grandpy_answer():
    grandpy = Grandpy()
    return jsonify({'answer': grandpy.grandpy_answer(request.form['user_raw_text'])})
