from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Variabila pentru baza de date SQLite
# utilizeaza obiect SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask('RepairStorageDevice')

    app.config['UPLOAD_FOLDER'] = 'backup'
    app.config['SECRET_KEY'] = 'app12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from modele import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

