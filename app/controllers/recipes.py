from flask import render_template, redirect, session, flash, request
from app.models.user import User
from app.models.recipe import Recipe
from app import app


#route to show add recipe html page
@app.route('/addrecipe')
def add_recipe_pg():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    return render_template('add_recipe.html')

#hidden route to create recipe
@app.route('/createrecipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    newRecipe = {
        'user_id' : session['user_id'],
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_30' : request.form['under_30'],
    }
    Recipe.insert(newRecipe)
    return redirect('/dashboard')

#edit page
@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    data = {
        'id': id,
    }
    recipe = Recipe.get_one(data)
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    if recipe.user_id != session['user_id']:
        flash('You did not create this recipe to be able to udpate it.')
        return redirect('/dashboard')
    return render_template('edit_recipe.html', recipe=recipe)
    
    
@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe_in_db(id):
    data = {
        "id" : id,
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "data_made" : request.form['date_made'],
        "under_30" : request.form['under_30'],
        "user_id" : request.form['user_id']
    }
    Recipe.update(data)
    return redirect('/dashboard')
