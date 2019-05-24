import os
from flask import Flask, render_template, redirect, request, url_for, session, flash, Blueprint
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'dcd-cookbook'
app.config["MONGO_URI"] = 'mongodb://admin:Xb0x3869@ds357955.mlab.com:57955/dcd-cookbook'
app.config["SECRET_KEY"] = 'SECRET_KEY'

mongo = PyMongo(app)

# results per page for pagination
per_page = 5

# main page
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    recipes = mongo.db.recipes.find().sort("recipe_title", 1).skip((page - 1) * per_page).limit(per_page)
    
    pagination = Pagination(page=page, per_page=per_page, total=recipes.count(), search=search, record_name='recipes', css_framework="bootstrap", bs_version=4)
    
    return render_template('recipes.html',
        recipes=recipes,
        pagination=pagination
        )

@app.route('/newest_recipes')
def newest_recipes():
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    recipes=mongo.db.recipes.find().sort("created", -1).skip((page - 1) * per_page).limit(per_page)
    
    pagination = Pagination(page=page, per_page=per_page, total=recipes.count(), search=search, record_name='recipes', bs_version=4)
    
    return render_template('recipes.html',
        recipes=recipes,
        pagination=pagination
        )


@app.route('/upvoted_recipes')
def upvoted_recipes():
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    recipes=mongo.db.recipes.find().sort("upvotes", -1).skip((page - 1) * per_page).limit(per_page)
    
    pagination = Pagination(page=page, per_page=per_page, total=recipes.count(), search=search, record_name='recipes', bs_version=4)
    
    return render_template('recipes.html',
        recipes=recipes,
        pagination=pagination
       )

@app.route('/vegetarian_recipes')
def vegetarian_recipes():
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    recipes=mongo.db.recipes.find({"is_vegetarian": "on"}).skip((page - 1) * per_page).limit(per_page)
    
    pagination = Pagination(page=page, per_page=per_page, total=recipes.count(), search=search, record_name='recipes', bs_version=4)
    
    return render_template('recipes.html',
        recipes=recipes,
        pagination=pagination
        )

@app.route('/vegan_recipes')
def vegan_recipes():
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    recipes=mongo.db.recipes.find({"is_vegan": "on"}).sort("upvotes", -1).skip((page - 1) * per_page).limit(per_page)
    
    pagination = Pagination(page=page, per_page=per_page, total=recipes.count(), search=search, record_name='recipes', bs_version=4)
    
    return render_template('recipes.html',
        recipes=recipes,
        pagination=pagination
        )

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
    if request.form.get('is_vegetarian', False):
        vegetarian = 'on'
    else:
        vegetarian = 'off'
    
    if request.form.get('is_vegan', False):
        vegan = 'on'
    else:
        vegan = 'off'
    
    allergens = []
    
    get_allergen_info(allergens)
    
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
        # checkbox list
        "is_vegetarian": vegetarian,
        "is_vegan": vegan,
        "allergen_info": allergens,
        "upvotes": 0,
        "upvoted_by": [],
        "created": datetime.now()
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
    
    if request.form.get('is_vegetarian', False):
        vegetarian = 'on'
    else:
        vegetarian = 'off'
    
    if request.form.get('is_vegan', False):
        vegan = 'on'
    else:
        vegan = 'off'
    
    allergens = []
    
    get_allergen_info(allergens)
    
    author = ''
    
    if 'username' in session:
        author = session['username']
    else:
        author = 'guest'
    
    recipes=mongo.db.recipes
    recipes.update_one( {'_id': ObjectId(recipe_id)},
    {
        '$set': 
        {
        "recipe_title": request.form['recipe_title'].lower(),
        "cuisine_type": request.form['cuisine_type'],
        "cook_time": request.form['cook_time'],
        "author_name": author,
        "ingredients_list": ingredients, # dictionary for ingredients
        "method_list": method_list,      # dictionary for method
        # checkbox list
        "is_vegetarian": vegetarian,
        "is_vegan": vegan,
        "allergen_info": allergens
        }
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
    
    upvotes = recipe['upvotes']
    
    # if not voted for this recipe append current user to list of upvoters
    current_upvoter = session['username']
    if current_upvoter not in upvoters:
        upvoters.append(current_upvoter)
        flash("Thank you for your vote")
        # update number of upvotes
        upvotes +=1
    else:
        flash("You have already voted for this recipe")
    
    # update database information
    recipes = mongo.db.recipes
    recipes.update_one( {'_id': ObjectId(recipe_id)},
    { '$set': {
        "upvoted_by": upvoters,
        "upvotes": upvotes
        }
    })
    
    return redirect(url_for('view_recipe', recipe_id=recipe['_id']))

@app.route('/custom_search')	
def custom_search():	
    return render_template('search.html',cuisine=mongo.db.cuisine.find())

@app.route('/search_page', methods=["POST"])
def search_page():
    
    user_input = request.form.to_dict()
    empty_flag = { # As in if no input is given
        "cookTimeSearch": "",
        "cuisineSearch": "",
        "ingredientField": "",
    }
    if user_input == empty_flag:
        flash("No results found, please expand your request")
        return redirect(url_for('custom_search'))
    ingredients = []
    for key, val in user_input.items():
        if 'ingredient' in key and len(val.strip()) > 0:
            ingredients.append(val)
    
    allergens = []
    
    get_allergen_info(allergens)

    q = {}
    q["$and"] = []
    
    # search by cooking time
    if len(request.form['cookTimeSearch']) > 0:
        q["$and"].append({"cook_time": {"$lt": request.form['cookTimeSearch'].strip()}})
    
    # search by cuisine origin
    if len(request.form['cuisineSearch']) > 0:
        q["$and"].append({"cuisine_type": {"$regex": request.form['cuisineSearch'].strip().lower()}})
    
    # search by ingredient
    if len(request.form['ingredientField']) > 0:
        q["$and"].append({"ingredients_list": {"$regex": request.form['ingredientField'].strip().lower()}})
    
    # search for allergens
    if allergens:
         q["$and"].append({"allergen_info": {"$nin": allergens}})
    
    if q != {}:
        recipes = mongo.db.recipes.find(q).sort([('created', -1)])
        session['q'] = q
        return redirect(url_for('search_results'))

@app.route('/search_results', methods=["GET"])
def search_results():
    
    q = session['q']
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    recipes=mongo.db.recipes.find(q).sort("created", -1).skip((page - 1) * per_page).limit(per_page)
    
    pagination = Pagination(page=page, per_page=per_page, total=recipes.count(), record_name='recipes', bs_version=4)
    
    return render_template('recipes.html',
        recipes=recipes,
        pagination=pagination
        )
    
# helper function for allergen information
def get_allergen_info(allergens):
    
    if request.form.get('has_gluten', False):
        allergens.append('gluten')
    else:
        pass
    
    if request.form.get('has_fish', False):
        allergens.append('fish')
    else:
        pass
    
    if request.form.get('has_nuts', False):
        allergens.append('nuts')
    else:
        pass
    
    if request.form.get('has_milk', False):
        allergens.append('milk')
    else:
        pass
    
    if request.form.get('has_shellfish', False):
        allergens.append('shellfish')
    else:
        pass
    
    if request.form.get('has_soy', False):
        allergens.append('soy')
    else:
        pass
    
    if request.form.get('has_wheat', False):
        allergens.append('wheat')
    else:
        pass
    
    return allergens

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)