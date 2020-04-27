'''
Clayton Brant (Remixt) 4/27/2020
This file serves as the backend to the ValorStats Webapp for the Game Valorant(Riot Games)
It connects to the riot games api and fetches game data (player and general game stats)
example url:
https://valorstats.com/api/v1/resources/riot?summoner=remixt&region=na1
DEBUG MODE:
http://127.0.0.1:5000/api/v1/resources/riot?summoner=remixt&region=na1
'''
import flask
import simplejson as json
from flask import request, jsonify
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

riot_url = ".api.riotgames.com" #url for contacting the riot games api, requires region in front of it. example: na1.api.riotgames.com
sum_url = "/lol/summoner/v4/summoners/by-name/" #url required for fetching data based on the summoner profile name
config = {} #config loaded in via JSON file (config.json), for now this only contains the api key required for fetching data from riot

with open('config.json') as json_file:
    config = json.load(json_file)
api_key = config['api_key']



@app.route('/', methods=['GET']) #default page
def home():
    return '''<h1>ValorStats API</h1>'''

@app.errorhandler(404) #errors are sent to 404 page
def page_not_found(e):
    return "<h1>404</h1>", 404

#valorant api isn't out yet, using league of legends summoner information as a placeholder
@app.route('/api/v1/resources/riot', methods=['GET'])
def api_filter():
    #build the full api request url from the parameters in the front end request
    query_parameters = request.args
    sum_name = query_parameters.get('summoner')
    region = query_parameters.get('region')

    query = str("https://"+region+riot_url+sum_url+sum_name+"?api_key="+api_key)

    results = requests.get(url = query) 
    results = json.loads(results.content)

    return jsonify(results)

app.run()