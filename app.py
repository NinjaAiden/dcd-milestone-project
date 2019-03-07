import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'dcd-cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:Xb0x3869@ds357955.mlab.com:57955/dcd-cookbook'

mongo = PyMongo(app)

@app.route('/')
def main():
    return "Hello World"

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)