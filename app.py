from datetime import datetime
from flask import Flask, render_template, request, request, jsonify, session
from dotenv import load_dotenv
from flask_session import Session
from Infrastructure.domain.entities import models
import os
import requests
import json

load_dotenv()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

AUTHORIZE_URL = os.getenv("RSO_BASE_URI") + "/authorize"
TOKEN_URL = os.getenv("RSO_BASE_URI") + "/token"
LOGOUT_URL = os.getenv("RSO_BASE_URI") + "/logout"
APP_CALLBACK_URL = os.getenv("APP_BASE_URL") +":"+ os.getenv("PORT") + os.getenv("APP_CALLBACK_PATH")
RSO_CLIENT_ID = os.getenv("RSO_CLIENT_ID")
AUTH_URL=AUTHORIZE_URL + "?redirect_uri=" + APP_CALLBACK_URL + "&client_id=" + RSO_CLIENT_ID + "&response_type=code" + "&scope=openid"

@app.route("/", methods=["POST","GET"])
def index(): 
    return render_template("index.html", AUTH_URL=AUTH_URL, LOGOUT_URL=LOGOUT_URL)

@app.route("/oauth-callback", methods=["POST","GET"])
def aouthCallback():
    code = request.args.get("code")

    data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": APP_CALLBACK_URL
    }

    try:
        req = requests.Session()
        req.auth = (os.getenv("RSO_CLIENT_ID"), os.getenv("RSO_CLIENT_SECRET"))

        r = req.post(
            url = TOKEN_URL, 
            data = data, 
            headers={"Content-Type":"application/x-www-form-urlencoded"},
            )

        session["token"] = r.json().get("access_token")

        return render_template("main.html", account={})   
    except Exception as e:
        print(f"Error token not generated {e}")

        return render_template("index.html", AUTH_URL=AUTH_URL, LOGOUT_URL=LOGOUT_URL)   

@app.route("/account", methods=["POST","GET"])
def account():

    if not session.get("token"): 
        return jsonify("Unauthorized"), 401   

    if request.method == "POST":
        requestURL = f"https://{os.getenv('REGION')}.api.riotgames.com/riot/account/v1/accounts/me"
        header = {"Authorization": "Bearer " + session["token"]}

        try:
            response = requests.get(requestURL, headers=header)

            if response.status_code != 200: 
                return render_template("main.html", ACCOUNT_INFO=response.json().get("status")["message"])

            
            return render_template("main.html", ACCOUNT_INFO=response.json())
        except:

            return render_template("main.html", ACCOUNT_INFO="Error getting account info ")

@app.route("/accounts/me", methods=["GET"])
def accountMe():

    if not session.get("token"): 
        return jsonify("Unauthorized"), 401   

    requestURL = f"https://{os.getenv('REGION')}.api.riotgames.com/riot/account/v1/accounts/me"
    header = {"Authorization": "Bearer " + session.get("token")}

    try:
        response = requests.get(requestURL, headers=header)

        if response.status_code != 200: 
            return jsonify("Internal Server Error"), 500  

        return response.json(), 200  
    except Exception as e:
            print(e)
            return jsonify("Internal Server Error"), 500  

@app.route("/summoners/overview", methods=["GET"])
def summonersOverview():

    region  = request.args.get("region", None)
    name  = request.args.get("name", None)

    if not os.getenv("APP_KEY"): 
        return jsonify("Internal Server Error"), 500   

    requestSummonerURL = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
    requestSummonerInfoURL = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/"
    header = {"X-Riot-Token": os.getenv("APP_KEY")}

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

if __name__ == "__main__" :
    app.run(port=os.getenv("PORT"), debug=True)


