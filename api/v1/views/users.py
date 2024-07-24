"""
Handles /api/v1/users endpoints
"""
from flask import jsonify, abort, make_response, request, redirect, url_for, redirect
from datetime import date
from api.v1.views import app_views, paginate
from models import storage
from models.user import User


@app_views.route("/users/<uuid:user_id>", strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Get user info"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user_repr = user.to_dict()
    del user_repr['__class__']
    del user_repr['password']
    return jsonify(user_repr)

@app_views.route("/users", strict_slashes=False, methods=['POST'])
def new_user():
     """Create new user account"""
     if not request.is_json:
         abort(400, 'Not a JSON')
     data = request.get_json()
     if "first_name" not in data or "last_name" not in data\
             or "email" not in data or "password" not in data\
             or "birth_date" not in data:
                abort(400, "Missing data")
     data['date_joined'] = str(date.today())
     if "gender" not in data:
         data['gender'] = 'U'
     if storage.check_user(data['email'], data['password']):
         return make_response(jsonify("The email or password has already been taken"), 409)
     new_user = User(**data)
     storage.add(new_user)
     storage.save()
     r = make_response(jsonify(new_user.to_dict()), 201)
     return r


@app_views.route("/users/<uuid:user_id>", strict_slashes=False, methods=['DELETE'])
def remove_user(user_id):
    """Delete user account"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    credentials = request.get_json()
    email = credentials.get("email", None)
    password = credentials.get("password", None)
    if not email or not password:
        abort(400, "Missing credentials")
    credential_user = storage.credential_user(email, password)
    if not credential_user:
        abort(400, "Wrong credentials")
    if credential_user.id != user.id:
        abort(401)
    storage.delete(user)
    return make_response(jsonify({}), 200)

@app_views.route("/users/<uuid:user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Update user info"""
    user_id = str(user_id)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    em = data.get("em", None)
    pawd = data.get("pawd", None)
    password = data.get("password", None)
    first_name = data.get("first_name", None)
    education = data.get("education", None)
    bio = data.get("bio", None)
    if not em or not pawd:
        abort(400, "Missing credentials")
    credential_user = storage.credential_user(em, pawd)
    if not credential_user:
        abort(400, "Wrong credentials")
    if user_id != credential_user.id:
            abort(401)
    if password or first_name or education or bio:
        allowed = ["password", "first_name", "education", "bio"]
        filtered_data = {}
        for k, v in data.items():
            if k not in allowed:
                pass
            else:
                filtered_data[k] = v
        user.update(**filtered_data)
        return make_response(jsonify(user.to_dict()), 200)
    abort(400, "Missing data")


@app_views.route("/users/<uuid:user_id>/questions", strict_slashes=False, methods=['GET'])
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

@app_views.route("/users/<uuid:user_id>/questions/<int:index>", strict_slashes=False, methods=['GET'])
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


@app_views.route("/users/<uuid:user_id>/answers", strict_slashes=False, methods=['GET'])
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

@app_views.route("/users/<uuid:user_id>/answers/<int:index>", strict_slashes=False, methods=['GET'])
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