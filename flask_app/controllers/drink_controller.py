from flask_app import app
from flask import render_template, redirect, request, flash, session
# from flask_app.models.user import User
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

import requests
import json


@app.route('/innerspirit')
def page_face():
    if 'query' in session:
        session.pop('query')
    return render_template('inner_spirit.html')

# @app.route('/results')
# def results():
#     return render_template('results.html', drinks = session['query'])

@app.route('/back_search')
def back_search():
    r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={session['search']}")
    j=r.json()
    print(j)
    if j == {'drinks': None}:
        print(j)
        flash('Cocktail NOT found')
        return redirect('/innerspirit')
    # session['query'] = (j['drinks'])
    data = (j['drinks'])
    return render_template('results.html', drinks=data)

@app.route('/search_cocktail', methods=['POST'])
def search_cocktail():
    search = request.form['search'].strip()
    session['search'] = search
    r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search}")
    j=r.json()
    print(j)
    if j == {'drinks': None}:
        print(j)
        flash('Cocktail NOT found')
        return redirect('/innerspirit')
    # session['query'] = (j['drinks'])
    data = (j['drinks'])
    return render_template('results.html', drinks=data)

@app.route('/description/<int:id>')
def search(id):
    r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={id}")
    j=r.json()
    obj = (j['drinks'][0])
    print(obj)
    session['ingredients'] = obj

    ingredients = []

    for x in range (1,16):
        key = 'strIngredient'+ str(x)
        if obj[key]:
            ingredients.append(obj[key])

    print(ingredients)

    specs = []

    for y in range (1,16):
        key = 'strMeasure' + str(y)
        if obj[key]:
            specs.append(obj[key])

    print(specs)


    return render_template('description.html', drink = session["ingredients"], ingredients = ingredients, specs=specs)




