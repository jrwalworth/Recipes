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
    return redirect('/dashboard/')