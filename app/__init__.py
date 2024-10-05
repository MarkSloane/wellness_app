from flask import Flask

app = Flask(__name__)

from app import routes

from app import app

@app.route('/')
def home():
    return "Welcome to the Wellness App!"

