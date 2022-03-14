from json import JSONEncoder
from flask import Flask
from flask import render_template
from flask import jsonify
from simplejson import JSONDecoder
import psycopg2
import pdb

app = Flask(__name__)
app.json_encoder = JSONEncoder

@app.route('/')
@app.route('/network')
def network():
    return render_template('network.html')