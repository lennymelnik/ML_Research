
from flask import Flask, render_template, url_for, flash, redirect, request, session

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>ABT Page</h1><p>You have no idea what you are doing</p>"

app.run()