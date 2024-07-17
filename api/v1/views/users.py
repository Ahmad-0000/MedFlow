"""
Handles /api/v1/users endpoints
"""
from flask import jsonify, abort, make_response, request, redirect, url_for, redirect
from datetime import date
from api.v1.views import app_views, paginate
from models import storage
from models.user import User



@app_views.route("/users/<uuid:user_id>", strict_slashes=False)
def get_user(user_id):
    """Get user info"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

# @app_views.route("/users", strict_slashes=False, methods=['POST'])
# def new_user():
#     """Create new user account"""
#     if not request.is_json:
#         abort(400, 'Not a JSON')
#     data = request.get_json()
#     if "first_name" not in data or "last_name" not in data\
#             or "email" not in data or "password" not in data\
#             or "birth_date" not in data:
#                 abort(400, "Missing data")
#     data['date_joined'] = str(date.today())
#     if "gender" not in data:
#         data['gender'] = 'U'
#     if storage.check_user(data['email'], data['password']):
#         return make_response(jsonify("The email or password has already been taken"), 409)
#     new_user = User(**data)
#     storage.add(new_user)
#     storage.save()
#     r = make_response(jsonify(new_user.to_dict()), 201)
#     r.set_cookie("id", new_user.id)
#     r.set_cookie("email", new_user.email)
#     r.set_cookie("password", new_user.password)
#     return r

@app_views.route("/users", strict_slashes=False, methods=['POST'])
def new_user():
    """Create a new user account"""
    data = request.form
    if "first_name" not in data or "last_name" not in data\
            or "email" not in data or "password" not in data\
            or "birth_date" not in data:
                abort(400, "Missing data")
    if "gender" not in data:
        data['gender'] = 'U'
    if storage.check_user(data['email'], data['password']):
        return make_response(jsonify("The email or password has already been taken"), 409)
    new_user = User(**data, date_joined=date.today())
    storage.add(new_user)
    storage.save()
    r = make_response("Account Created Successfully", 201)
    r.set_cookie("id", new_user.id)
    r.set_cookie("email", new_user.email)
    r.set_cookie("password", new_user.password)
    return r

@app_views.route("/login", strict_slashes=False, methods=['POST'])
def login():
    """Handeling Login form"""
    data = request.form
    if "email" not in data or "password" not in data:
        abort(400, "Missing data")
    user = storage.check_user(data['email'], data['password'])
    if not user:
        abort(404)
    r = make_response("You are logged in, you are now able to CRUD", 200)
    r.set_cookie("status", "In")
    r.set_cookie("id", user.id)
    r.set_cookie("email", user.email)
    r.set_cookie("password", user.password)
    return r

@app_views.route("/delete_account", strict_slashes=False, methods=['POST', 'GET'])
def delete_account():
    """Handles delete user account"""
    data = request.form
    if "email" not in data or "password" not in data:
        return make_response("Missing data")
    user = storage.check_user(data['email'], data['password'])
    if not user:
        make_response("No such user account", 404)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    if not email or not password:
        make_response("You are not the owner", 401)
    storage.delete(user)
    r = make_response("Account Deleted", 200)
    r.set_cookie("id", "", expires=0)
    r.set_cookie("email", "", expires=0)
    r.set_cookie("password", "", expires=0)
    return r

@app_views.route("/users/<uuid:user_id>", strict_slashes=False, methods=['DELETE'])
def remove_user(user_id):
    """Delete user account"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    return make_response(jsonify({}), 200)

@app_views.route("/users/<uuid:user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Update user info"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not request.is_json:
        abort(400, "Not a JSON")
    if not user:
        abort(404)
    data = request.get_json()
    allowed = ["password", "first_name", "education", "bio"]
    filtered_data = {}
    for k, v in data.items():
        if k not in allowed:
            pass
        else:
            filtered_data[k] = v
    user.update(**filtered_data)
    return make_response(jsonify(user.to_dict()), 200)
        

@app_views.route("/users/<uuid:user_id>/questions", strict_slashes=False)
def get_user_questions(user_id):
    """Get user questions"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    questions = user.questions
    questions_repr = []
    for question in questions:
        questions_repr.append(question.to_dict())
    return jsonify(questions_repr)

@app_views.route("/users/<uuid:user_id>/questions/<int:index>", strict_slashes=False)
def get_some_user_questions(user_id, index):
    """Get some user questions starting from <index> (included)"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    questions = user.questions
    questions_repr = []
    for question in questions:
        questions_repr.append(question.to_dict())
    some = paginate(questions_repr, 5, index)
    return jsonify(some)


@app_views.route("/users/<uuid:user_id>/answers", strict_slashes=False)
def get_user_answers(user_id):
    """Get user answers"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    answers = user.answers
    answers_repr = []
    for answer in answers:
        answers_repr.append(answer.to_dict())
    return jsonify(answers_repr)

@app_views.route("/users/<uuid:user_id>/answers/<int:index>", strict_slashes=False)
def get_some_user_answers(user_id, index):
    """Get some user answers"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    answers = user.answers
    answers_repr = []
    for answer in answers:
        answers_repr.append(answer.to_dict())
    some = paginate(answers_repr, 5, index)
    return jsonify(some)
