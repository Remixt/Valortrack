'''
'''
import flask
import simplejson as json
from flask import request, jsonify
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True
config = {}
with open('config.json') as json_file:
    config = json.load(json_file)
print(config['api_key'])
api_key = config['api_key']
riot_url = ".api.riotgames.com" #url for contacting the riot games api, requires region in front of it. example: na1.api.riotgames.com
sum_url = "/lol/summoner/v4/summoners/by-name/"
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>ValorStats API</h1>'''


@app.route('/api/v1/resources/pages/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('wikiscrape.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_pages = cur.execute('SELECT * FROM pages;').fetchall()
    try:
        for api_key in range(len(all_pages)):#format the inner json table
            all_pages[api_key]['table'] = json.loads(all_pages[api_key]['table'])
        return jsonify(all_pages)
    except:
        pass

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1>", 404


@app.route('/api/v1/resources/riot', methods=['GET'])
def api_filter():
    query_parameters = request.args

    sum_name = query_parameters.get('summoner')
    region = query_parameters.get('region')
    query = str("https://"+region+riot_url+sum_url+sum_name+"?api_key="+api_key)
    print(query)
    results = requests.get(url = query) 
    results = json.loads(results.content)
    return jsonify(results)
app.run()
#app.run(host="0.0.0.0")