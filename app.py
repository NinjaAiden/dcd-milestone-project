import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'dcd-cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:Xb0x3869@ds357955.mlab.com:57955/dcd-cookbook'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html',
        recipes=mongo.db.recipes.find())

@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe=the_recipe)

@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
        cuisine=mongo.db.cuisine.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes=mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)