import os
from flask import current_app, g
from json import JSONEncoder
from flask import Flask
from flask import render_template
from flask import jsonify
from simplejson import JSONDecoder
import sqlite3

DATABASE = 'spider.db'

app = Flask(__name__)
app.json_encoder = JSONEncoder

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, 'db', None)
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = make_dicts     
    return g.db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
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
            busnum || ' | ' || nodename as label
        FROM node WHERE networkid=?
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
        WHERE networkid=?
        """
    data = query_db(sql, params)
    return jsonify(data)

@app.route('/api/get_network_partial/<int:networkid>/<int:busnum>')
def api_get_network_partial(networkid, busnum):
    """Get network in the neighborhood of the specified node
    """
    params = (networkid, busnum, busnum)
    sql = """\
        SELECT 
            edgeid,
            edgename,
            frombusnum source,
            tobusnum target,
            ckt
        FROM edge 
        WHERE networkid=?
        AND (frombusnum=?
            OR tobusnum=?)
        """
    edges = query_db(sql, params)

    params = (busnum, busnum, busnum, busnum)
    sql = """\
        SELECT 
            nodeid,
            busnum,
            nodename,
            kv,
            busnum || ' | ' || nodename as label
        FROM node
        INNER JOIN edge 
            ON (edge.frombusnum = node.busnum
                AND edge.networkid = node.networkid)
        WHERE edge.frombusnum=? OR edge.tobusnum=?
        UNION
        SELECT 
            nodeid,
            busnum,
            nodename,
            kv,
            busnum || ' | ' || nodename as label
        FROM node
        INNER JOIN edge 
            ON (edge.tobusnum = node.busnum
                AND edge.networkid = node.networkid)
        WHERE edge.frombusnum=? OR edge.tobusnum=?
        """
    nodes = query_db(sql, params)

    eles = []
    for node in nodes:
        d = {'group': 'nodes', 'data': 
                {
                'id': node['busnum'], 
                'nodeid': node['nodeid'], 
                'busnum': node['busnum'], 
                'nodename': node['nodename'], 
                'label': node['label'], 
                'kv': node['kv']}
            }
        eles.append(d)
    
    for edge in edges:
        d = {'group': 'edges', 'data': {
                'edgeid': edge['edgeid'],
                'edgename': edge['edgename'],
                'source': edge['source'],
                'target': edge['target'],
                'ckt': edge['ckt']
                }
            }
        eles.append(d)
    # print(eles)
    return jsonify(eles)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
