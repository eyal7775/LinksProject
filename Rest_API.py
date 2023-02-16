from flask import Flask
import os
import json
import yaml

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/json', methods=['GET'])
def display_json():
    files = os.listdir(os.getcwd())
    paths = [os.path.join(os.getcwd(), basename) for basename in files]
    json_file = max(paths, key=os.path.getctime)
    with open(json_file, "r") as file:
        data = json.load(file)
    return data

@app.route('/yml', methods=['GET'])
def display_yml():
    files = os.listdir(os.getcwd())
    paths = [os.path.join(os.getcwd(), basename) for basename in files]
    yml_file = max(paths, key=os.path.getctime)
    with open(yml_file, "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def run():
    app.debug = True
    app.run()

# set FLASK_APP=C:\Users\eyal999\PycharmProjects\LinksProject\Rest_API.py
# $env:FLASK_APP = "C:\Users\eyal999\PycharmProjects\LinksProject\Rest_API.py"
# set FLASK_ENV=development
# set FLASK_DEBUG=True
# C:\Users\eyal999\AppData\Local\Programs\Python\Python311\python.exe -m flask --debug run