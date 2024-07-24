"""
Main app module
"""
from flask import Flask, make_response, request, redirect, render_template, abort, url_for
from datetime import date
from api.v1.views import app_views
from models import storage
from models.user import User
from models.question import Question
from models.answer import Answer
from models.comments import QueComment, AnsComment
from uuid import uuid4


flask_app = Flask(__name__)
cache_id = str(uuid4())
# Custom errors for error handling
errors = {
    'err_authorization': {
        'title': 'Unauthorized',
        'message': "You don't own this resource",
        'code': 401
    },
    'err_notfound': {
        'title': 'Not found',
        'message': "Not Found",
        'code': 404
    },
    'err_registeration': {
        'title': 'Not registered',
        'message': "You are not registered",
        'code': 403
    },
    'err_logging': {
        'title': 'Not logged',
        'message': "You are not logged in",
        'code': 403
    },
    'err_userconflict': {
        'title': 'Cookies issue',
        'message': "Don't mess up with your cookies",
        'code': 409
    },
    'err_taken': {
        'title': 'Already taken',
        'message': "The email or password has already been taken",
        'code': 409
    },
    'err_future': {
        'title': 'Future Date',
        'message': "Welcome from the future, however, you are not allowed to register :)",
        'code': 400
    }
}

@flask_app.route("/medflow/about", strict_slashes=False, methods=['GET'])
def about():
    """Render about page"""
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    return render_template("about.html", status=status, user_id=user_id, cache_id=cache_id)

@flask_app.route("/medflow/terms", strict_slashes=False, methods=['GET'])
def terms():
    """Renders terms of service page"""
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    return render_template("terms.html", status=status, user_id=user_id, cache_id=cache_id)

@flask_app.route("/medflow/privacy", strict_slashes=False, methods=['GET'])
def privacy():
    """Renders privacy policy page"""
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    return render_template("privacy.html", status=status, user_id=user_id, cache_id=cache_id)


def is_authenticated(user, request):
    """Check if the user of the request is authenticated"""
    status = request.cookies.get("status", None)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    if not email or not password:
        return (False, 403, 'err_registeration')
    credential_user = storage.credential_user(email, password, "h")
    if not credential_user:
        return (False, 403, 'err_registeration')
    if user.to_dict() != credential_user.to_dict():
        return (False, 409, 'err_userconflict')
    if status != "in":
        return (False, 403, 'err_logging')
    return (True, )

def is_item_owner(item, user):
    """Check if the item <item> is owned by the user <user>"""
    if item.user_id == user.id:
        return True
    return False


@flask_app.errorhandler(400)
def future_date(error):
    """Handle if the entered user birth date is from the future"""
    return make_response(render_template('error.html', error=errors['err_future'], cache_id=cache_id), 400)

@flask_app.errorhandler(401)
def unauthorized(error):
    """Handles 401 error"""
    return make_response(render_template("error.html", error=errors['err_authorization'], cache_id=cache_id), 401)

@flask_app.errorhandler(404)
def nf(error):
    """Handles 404 error"""
    return make_response(render_template('error.html', error=errors['err_notfound'], cache_id=cache_id), 404)

@flask_app.errorhandler(409)
def cookies_taken_issues(error):
    """
    Handling requests with messed cookies, or if the email or password
    are already taken
    """
    return make_response(render_template('error.html', error=errors[error.description], cache_id=cache_id), 409)

@flask_app.errorhandler(403)
def logging_registering_issues(error):
    """Handling requests without logging or registering"""
    return make_response(render_template('error.html', error=errors[error.description], cache_id=cache_id), 403)


@flask_app.teardown_appcontext
def refresh(exception):
    """Renewing the database session after each serve"""
    storage.close()

from web_flask.functionality.profile import *
from web_flask.functionality.authentication import *
from web_flask.functionality.question_interaction import *
from web_flask.functionality.question_comments import *
from web_flask.functionality.answer_interaction import *
from web_flask.functionality.answer_comments import *
