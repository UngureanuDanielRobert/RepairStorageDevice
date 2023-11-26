from flask import Flask,Blueprint,render_template,redirect,url_for,request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from init import db
from modele import User,Fisier
from flask_login import login_user,logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login',methods=['POST'])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if user or check_password_hash(user.password,password):
        login_user(user, remember=remember)
        return redirect(url_for('main.repairstorage'))

    flash('Contul nu este inregistrat.')
    return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup',methods=['POST'])
def signup_post():
    # validare user
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # daca email este deja inregistrat
    if user:
        flash('Exista deja contul')
        return redirect(url_for('auth.signup'))

    # creaza nou utilizator cu datele din formular
    new_user = User(email=email,name=name,password=generate_password_hash(password,method='scrypt'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
