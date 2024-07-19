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
    return render_template("terms.html", status=status, user_id=user_id)

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
        return (0, 0) # regfirst
    credentail_user = storage.check_user(email, password, "h")
    if not credentail_user:
        return (0, 0)
    if user.to_dict() != credentail_user.to_dict():
        return (0, 1) # userconflict
    if status != "in":
        return (0, 2) # logfirst
    return True

def is_item_owner(item, user):
    """Check if the item <item> is owned by the user <user>"""
    if item.user_id == user.id:
        return True
    return False


@flask_app.errorhandler(401)
def unauthorized(error):
    """Handles 401 error"""
    return make_response(render_template("unauthorized.html"), 401)

@flask_app.errorhandler(404)
def nf(error):
    """Handles 404 error"""
    return make_response(render_template('nf.html'), 404)

from web_flask.functionality.profile import *
from web_flask.functionality.authentication import *
from web_flask.functionality.question_interaction import *
from web_flask.functionality.question_comments import *
from web_flask.functionality.answer_interaction import *
from web_flask.functionality.answer_comments import *
