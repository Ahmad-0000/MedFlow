"""
Hanldes user-profile functionality
"""
from flask import make_response, request, redirect, render_template, abort
from flask import url_for
from models import storage
from models.user import User
from web_flask.app import flask_app, cache_id


@flask_app.route("/medflow/users/<uuid:user_id>", strict_slashes=False,
                 methods=['GET'])
def user_profile(user_id):
    """Render the profile of the user with the id <user_id>"""
    user_id = str(user_id)
    owner = storage.get(User, user_id)
    is_owner = None
    if not owner:
        abort(404)
    q = len(owner.questions)
    a = len(owner.answers)
    status = request.cookies.get("status", None)
    v_id = request.cookies.get("id", None)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    if not v_id or not email or not password:
        is_owner = False
        return render_template('profile.html', user=owner, status=status,
                               questions=q, answers=a, is_owner=is_owner)
    id_visiter = storage.get(User, v_id)
    credentail_visiter = storage.check_user(email, password, "h")
    if not id_visiter:
        is_owner = False
        return render_template('profile.html', user=owner, status=status,
                               questions=q, answers=a, is_owner=is_owner)
    if not credentail_visiter:
        is_owner = False
        return render_template('profile.html', user=owner, status=status,
                               questions=q, answers=a, is_owner=is_owner)
    if credentail_visiter.to_dict() != id_visiter.to_dict():
        is_owner = False
        return render_template('profile.html', user=owner, status=status,
                               questions=q, answers=a, is_owner=is_owner)
    if id_visiter.to_dict() == owner.to_dict():
        is_owner = True
    return render_template('profile.html', user=owner, status=status,
                           questions=q, answers=a, is_owner=is_owner)


@flask_app.route("/medflow/update_bio/<uuid:user_id>", strict_slashes=False,
                 methods=['GET'])
def udpate_bio(user_id):
    """Render the template for updating the bio"""
    return render_template("update_bio.html", user_id=user_id)


@flask_app.route("/medflow/update_bio_handler/<uuid:user_id>",
                 strict_slashes=False, methods=['POST'])
def update_bio_handler(user_id):
    """Update the user bio"""
    owner_id = str(user_id)
    status = request.cookies.get("status", None)
    visiter_id = request.cookies.get("id", None)
    v_email = request.cookies.get("email", None)
    v_password = request.cookies.get("password", None)
    if not status or status == "out":
        abort(403, 'err_logging')
    if not visiter_id or not v_email or not v_password:
        abort(403, 'err_registeration')
    owner = storage.get(User, owner_id)
    id_visiter = storage.get(User, visiter_id)
    credentail_visiter = storage.check_user(v_email, v_password, "h")
    if not owner:
        abort(404)
    if not id_visiter or not credentail_visiter:
        abort(403, 'err_registeration')
    if id_visiter.to_dict() != credentail_visiter.to_dict():
        abort(409, 'err_userconflict')
    if id_visiter.id != owner_id:
        abort(401)
    bio = request.form.get('body')
    owner.update(bio=bio)
    return redirect(url_for('user_profile', user_id=owner_id))


@flask_app.route("/medflow/update_edu/<uuid:user_id>", strict_slashes=False,
                 methods=['GET'])
def udpate_edu(user_id):
    """Render the template for updating the education info"""
    return render_template("update_edu.html", user_id=user_id)


@flask_app.route("/medflow/update_edu_handler/<uuid:user_id>",
                 strict_slashes=False, methods=['POST'])
def update_edu_handler(user_id):
    """Update the user edu"""
    owner_id = str(user_id)
    status = request.cookies.get("status", None)
    visiter_id = request.cookies.get("id", None)
    v_email = request.cookies.get("email", None)
    v_password = request.cookies.get("password", None)
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    if not visiter_id or not v_email or not v_password:
        return make_response(render_template('regfirst.html'), 403)
    owner = storage.get(User, owner_id)
    id_visiter = storage.get(User, visiter_id)
    credentail_visiter = storage.check_user(v_email, v_password, "h")
    if not owner:
        abort(404)
    if not id_visiter or not credentail_visiter:
        return make_response(render_template('regfirst.html'), 403)
    if id_visiter.to_dict() != credentail_visiter.to_dict():
        return make_response(render_template("userconflict.html"), 409)
    if id_visiter.id != owner_id:
        abort(401)
    edu = request.form.get('body')
    owner.update(education=edu)
    return redirect(url_for('user_profile', user_id=owner_id))
