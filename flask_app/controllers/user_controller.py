from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
# from flask_app.models.tv_show import Tv_show
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route('/login_page')
def reg_n_login():
    return render_template("login_reg.html")

@app.route('/register', methods=['POST'])
def register_user():

    if User.validate_user(request.form):
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password']),
        }
        User.create_user(data)

        users = User.get_user_by_email(request.form)
        user = users[0]
        session['user_id'] = user.id
        session['first_name'] = user.first_name
        return redirect('/innerspirit')


    else:
        print("is not valid")

    return redirect('/')

@app.route('/login', methods=['POST'])
def login_user():

    users = User.get_user_by_email(request.form)

    if len(users) != 1:
        flash("Incorrect Email or Password")
        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect Email or Password")
        return redirect('/') 

    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/dashboard')

@app.route('/dashboard')
def home_page():
    if 'user_id' not in session:
        flash('login to view page')
        return redirect('/')
    tv_shows = Tv_show.all_tv_shows()
    return render_template("homepage.html", tv_shows = tv_shows)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/innerspirit')

@app.route("/delete/<int:id>")
def delete_one_tv_show(id):
    data = {
        "id" : id
    }
    Tv_show.delete_tv_shows(data)
    return redirect('/dashboard')

@app.route('/viewshow/<int:id>')
def view_tv_show(id):
    if 'user_id' not in session:
        flash('login to view page')
        return redirect('/')
    data = {
        "id" : id
    }
    tv_shows=Tv_show.view_tv_show(data)
    return render_template("view_tv_show.html", tv_shows = tv_shows)

@app.route('/edit/<int:id>')
def render_edit(id):
    if 'user_id' not in session:
        flash('login to view page')
        return redirect('/')
    data = {
        "id" : id
    }
    tv_shows=Tv_show.view_tv_show(data)
    return render_template("edit_tv_show.html", id = id, tv_shows = tv_shows)

@app.route('/edittvshow', methods=['POST'])
def edit_tv_show():
    if Tv_show.validate_tv_show(request.form):
        data = {
            'id' : request.form['id'],
            'title' : request.form['title'],
            'network' : request.form['network'],
            'release_date' : request.form['release_date'],
            'description' : request.form['description'],
        }
        Tv_show.edit_tv_show(data)
        return redirect('/dashboard')

    else:
        id = request.form['id']

        print("is not valid")
        return redirect(f'/edit/{id}')