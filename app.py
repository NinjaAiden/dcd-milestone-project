import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'dcd-cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:Xb0x3869@ds357955.mlab.com:57955/dcd-cookbook'
app.config["SECRET_KEY"] = 'SECRET_KEY'

mongo = PyMongo(app)

# main page
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html',
        recipes=mongo.db.recipes.find())

# login page
@app.route('/login', methods=['GET','POST'])
def login():
    
    # check if user is logged in
    if 'username' in session:
        return redirect('/')
    
    # check login details
    if request.method == "POST":
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})
        if login_user and login_user['password'] == request.form['password']:
            session['username'] = request.form['username']
            return redirect('/')
        else:
            # show message if password incorrect
            flash("Invalid username/password combination, please try again", category='error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    # check if user is logged in
    if 'username' in session:
        return redirect('/')

    if request.method == 'POST':
        
        if request.form['guest']:
            flash('This is a reserved name, please choose a different name')
        
        # Check if username exists in database                                                                
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        
        # if user name does not exist, add to database
        if existing_user is None:
            users.insert_one({'username': request.form['username'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect('/')
        else:
            flash("Username already exists. Please choose a different name")
        
    return render_template('register.html')

# route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

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
        if i == "":
            pass
        else:
            ingredients.append(i)
    
    # form method into a dictionary
    method_list = []
   
    method = request.form.getlist('method')
    
    for m in method:
        if m == "":
            pass
        else:
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

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', recipe=the_recipe)

@app.route('/update_recipe')
def update_recipe():
    
    # form ingredients into a dictionary
    ingredients = []
    
    ingredient = request.form.getlist('ingredient')
    
    for i in ingredient:
        if i == "":
            pass
        else:
            ingredients.append(i)
    
    # form method into a dictionary
    method_list = []
   
    method = request.form.getlist('method')
    
    for m in method:
        if m == "":
            pass
        else:
            method_list.append(m)
    
    # Reorganise all data into one dictionary before inserting into database
    data = {
        "recipe_title": request.form['recipe_title'].lower(),
        "cuisine_type": request.form['cuisine_type'],
        "cook_time": request.form['cook_time'],
        "ingredients_list": ingredients, # dictionary for ingredients
        "method_list": method_list # dictionary for method
    }
    
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)