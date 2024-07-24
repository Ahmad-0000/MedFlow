"""
Handle /api/v1/answers endpoint
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.answer import Answer
from models.question import Question


@app_views.route("/answers/<uuid:answer_id>", strict_slashes=False)
def get_answer(answer_id):
    """Get the answer with id <answer_id>"""
    answer_id = str(answer_id)
    answer = storage.get(Answer, answer_id)
    if not answer:
        abort(404)
    return jsonify(answer.to_dict())


@app_views.route("/answers/<uuid:question_id>/<int:index>", strict_slashes=False)
def get_some_answers(question_id, index):
    """
    Get the answers 5 answers starting from index <index> (included)
    of the question with id <question_id>
    """
    some_answers = storage.some(Answer, index)
    answers_repr = []
    for ans in some_answers:
        answers_repr.append(ans.to_dict())
    return jsonify(answers_repr)

@app_views.route("/answers/<uuid:answer_id>/comments", strict_slashes=False)
def get_answer_comments(answer_id):
    """Get comments of the answer with id <answer_id>"""
    answer_id = str(answer_id)
    answer = storage.get(Answer, answer_id)
    if not answer:
        abort(404)
    comments = answer.comments
    comments_repr = []
    for c in comments:
        comments_repr.append(c.to_dict())
    return jsonify(comments_repr)

@app_views.route("/answers", strict_slashes=False, methods=["POST"])
def new_answer():
    """Create a new answer"""
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    question_id = data.get('question_id', None)
    email = data.get("email", None)
    password = data.get("password", None)
    body = data.get("body", None)
    if not email or not password or not body or not question_id:
        abort(400, "Missing data")
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    credential_user = storage.credential_user(email, password)
    if not credential_user:
        abort(400, "Wrong credentials")
    answer = Answer(user_id=credential_user.id, question_id=question.id, body=body)
    storage.add(answer)
    storage.save()
    return make_response(jsonify(answer.to_dict()), 201)

@app_views.route("/answers/<uuid:answer_id>", strict_slashes=False, methods=['PUT'])
def update_answer(answer_id):
    """Update answer with id <answer_id>"""
    answer_id = str(answer_id)
    answer = storage.get(Answer, answer_id)
    if not answer:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    body = data.get("body", None)
    if not email or not password or not body:
        abort(400, "Missing data")
    credential_user = storage.credential_user(email, password)
    if not credential_user:
        abort(400, "Wrong credentials")
    if credential_user.id != answer.user_id:
        abort(401)
    answer.update(body=body)
    return make_response(jsonify(answer.to_dict()), 200)

@app_views.route("/answers/<uuid:answer_id>", strict_slashes=False, methods=['DELETE'])
def delete_answer(answer_id):
    """Delete answer with id <answer_id>"""
    answer_id = str(answer_id)
    answer = storage.get(Answer, answer_id)
    if not answer:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    if not email or not password:
        abort(400, "Missing credentials")
    credential_user = storage.credential_user(email, password)
    if not credential_user:
        abort(400, "Wrong credentials")
    if credential_user.id != answer.user_id:
        abort(401)
    storage.delete(answer)
    return make_response(jsonify({}), 200)