from flask import Flask, request
from App_Service import App_Service
import json

app = Flask(__name__)
appService = App_Service()

@app.route('/recommend_post', methods=['POST'])
def recommend_post():
    request_data = request.get_json()

    user = request_data['user']

    return json.dumps(appService.recommend_post_to_user(user, 4))


@app.route('/people_interested', methods=['POST'])
def people_interested_in_topic():
    request_data = request.get_json()

    topic = request_data['topic']

    return json.dumps(appService.people_interested_in_topic(topic, 10))


@app.route('/common_interests', methods=['POST'])
def find_interests():
    request_data = request.get_json()

    profile = request_data['profile']

    return json.dumps(appService.find_interests(profile, 10))


@app.route('/num_followers', methods=['POST'])
def num_followers():
    request_data = request.get_json()

    profile = request_data['profile']

    return json.dumps(appService.num_followers(profile))

@app.route('/followers_reach', methods=['POST'])
def followers_reach():
    request_data = request.get_json()

    profile = request_data['profile']

    return json.dumps(appService.followers_reach(profile))

@app.route('/influential_taste', methods=['GET'])
def influential_taste():

    return json.dumps(appService.influential_taste(7))


@app.route('/')
def home():
    return "App Works!!!"


