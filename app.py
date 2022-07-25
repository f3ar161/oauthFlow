from contextlib import redirect_stderr
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

#models
from internal.domain.entities import models

import os
import requests
import json

load_dotenv()
app = Flask(__name__)

AUTHORIZE_URL = os.getenv("RSO_BASE_URI") + "/authorize"
TOKEN_URL = os.getenv("RSO_BASE_URI") + "/token"
LOGOUT_URL = os.getenv("RSO_BASE_URI") + "/logout"
APP_CALLBACK_URL = os.getenv("APP_BASE_URL") +":"+ os.getenv("PORT") + os.getenv("APP_CALLBACK_PATH")
RSO_CLIENT_ID = os.getenv("RSO_CLIENT_ID")
AUTH_URL=AUTHORIZE_URL + "?redirect_uri=" + APP_CALLBACK_URL + "&client_id=" + RSO_CLIENT_ID + "&response_type=code" + "&scope=openid"



@app.route('/', methods=['POST','GET'])
def index(): 
    return render_template('index.html', AUTH_URL = AUTH_URL, LOGOUT_URL=LOGOUT_URL)

@app.route('/oauth-callback', methods=['POST','GET'])
def aouthCallback():
    code = request.args.get('code')

    data = {
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': APP_CALLBACK_URL
        }

    try:
        session = requests.Session()
        session.auth = (os.getenv('RSO_CLIENT_ID'), os.getenv('RSO_CLIENT_SECRET'))

        r = session.post(
            url = TOKEN_URL, 
            data = data, 
            headers={"Content-Type":"application/x-www-form-urlencoded"},
            )

        os.environ["TOKEN"] = r.json().get('access_token')

        return render_template('main.html', account={})   
    except:
        return render_template('index.html', AUTH_URL = AUTH_URL, LOGOUT_URL=LOGOUT_URL)   


@app.route('/account', methods=['POST','GET'])
def account():

    if request.method == 'POST':
        requestURL = "https://" + os.getenv('REGION') + ".api.riotgames.com/riot/account/v1/accounts/me"
        header = {"Authorization": 'Bearer ' + os.getenv('TOKEN')}

        try:
            response = requests.get(requestURL, headers=header)

            if response.status_code != 200: 
                return render_template('main.html', ACCOUNT_INFO = response.json().get('status')["message"])

            
            return render_template('main.html', ACCOUNT_INFO = response.json())
        except:

            return render_template('main.html', ACCOUNT_INFO = "Error getting account info ")


@app.route('/accounts/me', methods=['GET'])
def accountMe():

    ## validate token 
    if os.getenv('TOKEN') != "": 

        requestURL = "https://" + os.getenv('REGION') + ".api.riotgames.com/riot/account/v1/accounts/me"
        header = {"Authorization": 'Bearer ' + os.getenv('TOKEN')}

        try:
            response = requests.get(requestURL, headers=header)

            if response.status_code != 200: 
                return jsonify("Not data was found"), 401  

            return response.json(), 200  
        except:

            return jsonify("Internal Server Error"), 500  

    return jsonify("Authentication process is missing"), 500   


@app.route('/summoners/overview', methods=['GET'])
def summonersOverview():

    region  = request.args.get('region', None)
    name  = request.args.get('name', None)

    ## validate token 
    if os.getenv('TOKEN') != "": 

        requestSummonerURL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name
        requestSummonerInfoURL = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/"
        header = {"X-Riot-Token": os.getenv('APP_KEY')}

        try:
            response = requests.get(requestSummonerURL,headers=header)
            
            summoner = models.Summoner(
                response.json().get("id"),
                response.json().get("name"),
                response.json().get("profileIconId"),
                response.json().get("summonerLevel"),
                datetime.utcfromtimestamp(response.json().get("revisionDate")/ 1000.0),
                []
            )

            requestSummonerInfoURL += summoner.id
            responseEntries = requests.get(requestSummonerInfoURL,headers=header)

            summoner.leagueEntries = responseEntries.json()

            return json.dumps(vars(summoner),indent=0, sort_keys=True, default=str), 200  
        except Exception as e:
            print(e)
            return jsonify("Internal Server Error"), 500  

    return jsonify("Authentication process is missing"), 500   


if __name__ == "__main__" :
    app.run(port=os.getenv("PORT"), debug=True)


