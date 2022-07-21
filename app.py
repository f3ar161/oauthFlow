from contextlib import redirect_stderr
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


db = SQLAlchemy(app)

APP_KEY = 'RGAPI-e328d0b8-3449-4727-960b-6848863a00bf' 
APP_BASE_URL = 'http://local.testingapp.com:5000'
APP_CALLBACK_PATH = "/oauth-callback"

product_name = 'test-api-calls'
second_api_key = 'd3954acc-f0c8-4ed4-ac24-7b26e5f12e15'


##riot urls 
RSO_BASE_URI = "https://auth.riotgames.com"
AUTHORIZE_URL = RSO_BASE_URI + "/authorize"
TOKEN_URL = RSO_BASE_URI + "/token"
LOGOUT_URL = RSO_BASE_URI + "/logout"
APP_CALLBACK_URL = APP_BASE_URL + APP_CALLBACK_PATH

######### import commands ##########
## python 
## from app import db
## db.create_all()

class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    sing_url = db.Column(db.String(3000), nullable=False)
    access_token = db.Column(db.String(1500))
    refresh_token = db.Column(db.String(1500))
    scope = db.Column(db.String(1500))
    id_token = db.Column(db.String(1500))
    token_type = db.Column(db.String(1500))
    token_type = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    
    ##new_task = Todo(sing_url=AUTHORIZE_URL + "?redirect_uri=" + APP_CALLBACK_URL + "&client_id=" + "riot-example-app" + "&response_type=code" + "&scope=openid")
    ##db.session.add(new_task)
    ##db.session.commit()
    
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was a problem deleting that task'

@app.route('/request', methods=['GET'])
def rerquest():
    singUrl = AUTHORIZE_URL + "?redirect_uri=" + APP_CALLBACK_URL + "&client_id=" + "riot-example-app" + "&response_type=code" + "&scope=openid"
    
    return singUrl


@app.route('/oauth-callback')
def aouthCallback():

    # here we want to get the value of user (i.e. ?user=some-value)
    code = request.args.get('code')

    # data to be sent to api
    data = {
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': APP_CALLBACK_URL
        }
  
    # sending post request and saving response as response object
    session = requests.Session()
    session.auth = ("RSO_CLIENT_ID", "RSO_CLIENT_SECRET")

    r = session.post(
        url = TOKEN_URL, 
        data = data, 
        headers={"Content-Type":"application/x-www-form-urlencoded"},
        auth=("RSO_CLIENT_ID", "RSO_CLIENT_SECRET")
        )
    
    return r

@app.route('/riot.txt', methods=['GET'])
def test():    
    
    return "909ed1a4-6c0f-4bc7-9130-f1eaae60b1e7"

       

if __name__ == "__main__" :
    app.run(port= 5000, debug=True)


