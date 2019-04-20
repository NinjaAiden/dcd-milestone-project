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

# registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    # check if user is logged in
    if 'username' in session:
        return redirect('/')

    if request.method == 'POST':
        
        if request.form['username'] == 'guest':
            flash('This is a reserved name, please choose a different name')
            return render_template('register.html')
        
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
@app.route('/insert_recipe', methods=['GET','POST'])
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
    
    # check if checkboxes are checked
    
    vegetarian = ''
    vegan = request.form.get('is_vegetarian')
    
    if request.form.get('is_vegetarian', False):
        vegetarian = 'on'
    else:
        vegetarian = 'off'
    
    if request.form.get('is_vegan', False):
        vegan = 'on'
    else:
        vegan = 'off'
    
    # check if user is signed in
    
    author = ''
    
    if 'username' in session:
        author = session['username']
    else:
        author = 'guest'
    
    if request.form.get('cuisine_type') == None:
        flash('PLease select a valid option')
    
    # Reorganise all data into one dictionary before inserting into database
    
    data = {
        "recipe_title": request.form['recipe_title'].lower(),
        "cuisine_type": request.form['cuisine_type'],
        "cook_time": request.form['cook_time'],
        "author_name": author,
        "ingredients_list": ingredients, # dictionary for ingredients
        "method_list": method_list, # dictionary for method
        "is_vegetarian": vegetarian,
        "is_vegan": vegan,
        "upvotes": "0",
        "upvoted_by": []
    }

    recipes.insert_one(data)
    
    return redirect(url_for('get_recipes'))

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_cuisine=mongo.db.cuisine.find()
    return render_template('editrecipe.html', recipe=the_recipe, cuisine=all_cuisine)

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    
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
    
    author = ''
    
    vegetarian = ''
    vegan = ''
    
    if request.form.get('is_vegetarian', False):
        vegetarian = 'on'
    else:
        vegetarian = 'off'
    
    if request.form.get('is_vegan', False):
        vegan = 'on'
    else:
        vegan = 'off'
    
    if 'username' in session:
        author = session['username']
    else:
        author = 'guest'
    
    recipes=mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "recipe_title": request.form['recipe_title'].lower(),
        "cuisine_type": request.form['cuisine_type'],
        "cook_time": request.form['cook_time'],
        "author_name": author,
        "ingredients_list": ingredients, # dictionary for ingredients
        "method_list": method_list,      # dictionary for method
        "is_vegetarian": vegetarian,
        "is_vegan": vegan
    })
    
    return redirect(url_for('get_recipes'))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

@app.route('/upvote_recipe/<recipe_id>', methods=['GET', 'POST'])
def upvote_recipe(recipe_id):
    
    # get recipe information from database
    recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    # get list of upvoters
    upvoters = recipe['upvoted_by']
    
    # append current user to list of upvoters
    current_upvoter = session['username']
    upvoters.append(current_upvoter)
    
    # get number of upvotes and parse to integer
    upvote_int = int(recipe['upvotes'])
    
    # update number of upvotes
    upvote_int +=1
    
    # parse upvotes back to string
    upvote_string= str(upvote_int)
    
    # update database information
    recipes = mongo.db.recipes
    recipes.update_one( {'_id': ObjectId(recipe_id)},
    { '$set': {
        "upvoted_by": upvoters,
        "upvotes": upvote_string
        }
    })
    
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)