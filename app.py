import os
from flask import current_app, g
from json import JSONEncoder
from flask import Flask
from flask import render_template
from flask import jsonify
from simplejson import JSONDecoder
import psycopg2
import psycopg2.extras
import pdb
# from urllib.parse import urlparse

DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.json_encoder = JSONEncoder

def get_db():
    # result = urlparse(DATABASE_URL)
    if 'db' not in g:
        # current_app.config['DATABASE'],
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

def query_db(query, args=(), one=False):
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@app.route('/')
@app.route('/network')
def network():
    return render_template('network.html')

@app.route('/hello')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/hello_vue')
def hello_vue():
    return render_template('hello_vue.html')

@app.route('/api/list_networks')
def api_list_network():
    rows = query_db("SELECT * FROM network")
    data = jsonify(rows)
    return data

@app.route('/api/list_nodes/<int:networkid>')
def api_list_node(networkid):
    params = (networkid, )
    sql = """\
        SELECT nodeid,nodename,kv,busnum,
            CONCAT(busnum, ' | ', nodename) as label
        FROM node WHERE networkid=%s
        """
    data = query_db(sql, params)
    return jsonify(data)

@app.route('/api/list_edge/<int:networkid>')
def api_list_edge(networkid):
    params = (networkid, )
    sql = """\
        SELECT 
            edgename,
            frombusnum source,
            tobusnum target,
            ckt 
        FROM edge 
        WHERE networkid=%s
        """
    data = query_db(sql, params)
    return jsonify(data)

@app.route('/api/get_network_partial/<int:networkid>/<int:nodeid>')
def api_get_network_partial(networkid):
    return

@app.route('/api/get_network_all/<int:networkid>')
def api_get_network_all(networkid):
    params = (networkid, )
    sql = """\
        SELECT 
            edgename,
            frombusnum source,
            tobusnum target,
            ckt
        FROM edge 
        WHERE networkid=%s
        """
    edges = query_db(sql, params)

    sql = """\
        SELECT 
            busnum,
            nodename,
            kv,
            CONCAT(busnum, ' | ', nodename) as label
        FROM node
        WHERE networkid=%s
        """
    nodes = query_db(sql, params)

    eles = []
    for node in nodes:
        d = {'group': 'nodes', 'data': 
                {'id': node['busnum'], 
                'nodename': node['nodename'], 
                'label': node['label'], 
                'kv': node['kv']}
            }
        eles.append(d)
    
    for edge in edges:
        d = {'group': 'edges', 'data': {
                'source': edge['source'],
                'target': edge['target'],
                'ckt': edge['ckt']
                }
            }
        eles.append(d)
    print(eles)
    return jsonify(eles)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
