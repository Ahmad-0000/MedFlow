"""
Handles user authentication
"""
from flask import make_response, request, redirect, render_template, abort
from flask import url_for
from datetime import date
from models import storage
from models.user import User
from web_flask.app import flask_app, cache_id


@flask_app.route("/medflow/register", methods=['GET'], strict_slashes=False)
def register():
    """Render register page"""
    return render_template('register.html', cache_id=cache_id)


@flask_app.route("/medflow/create_account", strict_slashes=False,
                 methods=['POST'])
def register_handler():
    """Create a new user account"""
    data = request.form
    if "first_name" not in data or "last_name" not in data\
            or "email" not in data or "password" not in data\
            or "birth_date" not in data:
        abort(400, "Missing data")
    if storage.check_user(data['email'], data['password']):
        abort(409, 'err_taken')
    bd = data['birth_date']
    if bd > str(date.today()):
        abort(400)
    if "gender" not in data:
        new_user = User(**data, date_joined=date.today(), gender="U")
    else:
        new_user = User(**data, date_joined=date.today())
    storage.add(new_user)
    storage.save()
    r = make_response(redirect(url_for('user_profile', user_id=new_user.id)),
                      201)
    r.set_cookie("id", new_user.id, max_age=108000)
    r.set_cookie("email", new_user.email, max_age=108000)
    r.set_cookie("password", new_user.password, max_age=108000)
    r.set_cookie("status", "in", max_age=108000)
    return r


@flask_app.route("/medflow/delete", strict_slashes=False, methods=['GET'])
def delete():
    """Renders delete account page"""
    return render_template("delete_account.html", cache_id=cache_id)


@flask_app.route("/medflow/logout", strict_slashes=False, methods=['GET'])
def logout():
    """Handles user's logging out"""
    r = make_response(redirect(url_for("questions_page")))
    r.set_cookie("status", "", expires=0)
    return r


@flask_app.route("/medflow/login_page", strict_slashes=False, methods=['GET'])
def login_page():
    """Renders login page"""
    return render_template("login.html", cache_id=cache_id)


@flask_app.route("/medflow/login", strict_slashes=False, methods=['POST'])
def login():
    """Handle user's logging in"""
    data = request.form
    user = storage.credential_user(data['email'], data['password'])
    if not user:
        abort(404)
    r = make_response(redirect(url_for('user_profile', user_id=user.id)), 200)
    r.set_cookie("id", user.id, max_age=108000)
    r.set_cookie("email", user.email, max_age=108000)
    r.set_cookie("password", user.password, max_age=108000)
    r.set_cookie("status", "in", max_age=108000)
    return r


@flask_app.route("/medflow/delete_account", strict_slashes=False,
                 methods=['POST'])
def delete_account():
    """Deletes user's account"""
    data = request.form
    user = storage.credential_user(data['email'], data['password'])
    if not user:
        abort(404)
    storage.delete(user)
    r = make_response(redirect(url_for("questions_page")), 200)
    r.set_cookie("status", "", expires=0)
    r.set_cookie("id", "", expires=0)
    r.set_cookie("email", "", expires=0)
    r.set_cookie("password", "", expires=0)
    return r