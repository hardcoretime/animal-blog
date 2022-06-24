from os import getenv

from flask import Flask, url_for, redirect, render_template
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate

from models import db, User
from views.auth import auth_app
from views.posts import posts_app

app = Flask(__name__)
CONFIG_NAME = getenv("CONFIG", "DevelopmentConfig")
app.config.from_object(f"config.{CONFIG_NAME}")

app.register_blueprint(posts_app, url_prefix="/posts")
app.register_blueprint(auth_app, url_prefix="/auth")

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth_app.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.cli.command('create-schemas', help='Creates all known schemas')
def create_all_schemas():
    print('create all tables...')
    db.create_all()
    print('created all tables!')


@app.cli.command('drop-schemas', help='Drop all known schemas')
def drop_all_schemas():
    print('drop all tables...')
    db.drop_all()
    print('dropped all tables!')


@app.route("/")
def posts_list():
    url_posts = url_for("posts_app.list")
    return redirect(url_posts)


@app.route("/profile/", endpoint="profile")
@login_required
def profile():
    return render_template('auth/profile.html', name=current_user.name)


if __name__ == '__main__':
    app.run()
