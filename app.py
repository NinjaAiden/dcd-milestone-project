import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'dcd-cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:Xb0x3869@ds357955.mlab.com:57955/dcd-cookbook'

mongo = PyMongo(app)

# main page
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html',
        recipes=mongo.db.recipes.find())

# page to view recipe in full
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe=the_recipe)

# page to render form for adding recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
        cuisine=mongo.db.cuisine.find())

# page to collate data to database
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    # get database collection
    recipes=mongo.db.recipes
    
    # form ingredients into a dictionary
    ingredients = []
    
    ingredient = request.form.getlist('ingredient')
    
    for i in ingredient:
        ingredients.append(i)
    
    # form method into a dictionary
    method_list = []
   
    method = request.form.getlist('method')
    
    for m in method:
        method_list.append(m)
    
    # Reorganise all data into one dictionary before inserting into database
    data = {
        "recipe_title": request.form['recipe_title'].lower(),
        "cuisine_type": request.form['cuisine_type'],
        "cook_time": request.form['cook_time'],
        "ingredients_list": ingredients, # dictionary for ingredients
        "method_list": method_list # dictionary for method
    }

    recipes.insert_one(data)
    
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)