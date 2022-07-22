from contextlib import redirect_stderr
from datetime import datetime
from email import header
from flask import Flask, redirect, render_template, request, url_for, request
from dotenv import load_dotenv

import os
import requests

load_dotenv()
app = Flask(__name__)

AUTHORIZE_URL = os.getenv("RSO_BASE_URI") + "/authorize"
TOKEN_URL = os.getenv("RSO_BASE_URI") + "/token"
LOGOUT_URL = os.getenv("RSO_BASE_URI") + "/logout"
APP_CALLBACK_URL = os.getenv("APP_BASE_URL") +":"+ os.getenv("PORT") + os.getenv("APP_CALLBACK_PATH")
RSO_CLIENT_ID = os.getenv("RSO_CLIENT_ID")


@app.route('/', methods=['POST','GET'])
def index(): 
    return render_template('index.html', AUTH_URL=AUTHORIZE_URL + "?redirect_uri=" + APP_CALLBACK_URL + "&client_id=" + RSO_CLIENT_ID + "&response_type=code" + "&scope=openid", LOGOUT_URL=LOGOUT_URL)

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
        return render_template('logout.html', LOGOUT_URL=LOGOUT_URL)   

@app.route('/account', methods=['POST','GET'])
def account():

    if request.method == 'POST':
        requestURL = "https://" + os.getenv('REGION') + ".api.riotgames.com/riot/account/v1/accounts/me"
        header = {"Authorization": 'Bearer ' + os.getenv('TOKEN')}

        try:
            response = requests.get(requestURL, headers=header)

            if response.json().get('status')["status_code"] != 200: 
                return render_template('main.html', ACCOUNT_INFO = response.json().get('status')["message"])

            return render_template('main.html', ACCOUNT_INFO = response.json())
        except:
            return render_template('main.html', ACCOUNT_INFO = "Error getting account info")
   

if __name__ == "__main__" :
    app.run(port= 5000, debug=True)


