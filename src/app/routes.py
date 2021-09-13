from flask import render_template, request, jsonify, redirect, request, url_for
from app import app
from app import database as db_helper
import requests
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from app import User as usr_model
import json


db_helper.create_tables()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

login_manager = LoginManager()
login_manager.init_app(app)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    data = request.get_json()
    valid_fields = ['status', 'task', 'difficulty', 'importance', 'deadline']
    try:
        if fields_to_update := list(set(data) & set(valid_fields)):
            for field in fields_to_update:
                db_helper.update_task(field, task_id, data[field])
                result = {'success': True, 'response': f'{field.title()} Updated'}

            priority = 100 - (round((int(data['difficulty']) + (10-int(data['importance'])) + int(data['deadline'])) / 3, 2) * 10)
            db_helper.update_task('priority', task_id, priority)
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    db_helper.insert_new_task(current_user.id, data['task'], data['difficulty'], data['deadline'], data['importance'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@login_manager.user_loader
def load_user(user_id):
    return usr_model.User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/")
def index():
    if current_user.is_authenticated:
        items = db_helper.fetch_todo(current_user.id)
        print(items)
        return render_template("index.html", items=items)
    else:
        return render_template("unauthorized.html")


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))


    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)


    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = usr_model.User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    if not usr_model.User.get(unique_id):
        usr_model.User.create(unique_id, users_name, users_email, picture)

    login_user(user)

    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
