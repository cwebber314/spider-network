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

@app.route('/hello')
def hello_world():
    return "<p>Hello, World!</p>"
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
