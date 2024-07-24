"""
Handles /api/v1/comments endpoint
"""
from flask import make_response, jsonify, abort, request
from models import storage
from models.question import Question
from models.answer import Answer
from models.comments import AnsComment, QueComment
from api.v1.views import app_views


@app_views.route("/comments/questions/<uuid:question_id>", strict_slashes=False, methods=['POST'])
def new_question_comment(question_id):
    """Add a comment for the question with id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
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
    q_comment = QueComment(user_id=credential_user.id, question_id=question_id, body=body)
    storage.add(q_comment)
    storage.save()
    return make_response(jsonify(q_comment.to_dict()), 201)

@app_views.route("/comments/questions/<uuid:comment_id>", strict_slashes=False, methods=['PUT'])
def update_question_comment(comment_id):
    """Update the qustion comment with the id <comment_id>"""
    comment_id = str(comment_id)
    comment = storage.get(QueComment, comment_id)
    if not comment:
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
    if credential_user.id != comment.user_id:
        abort(401)
    comment.update(body=body)
    return make_response(jsonify(comment.to_dict()), 200)


@app_views.route("/comments/questions/<uuid:comment_id>", strict_slashes=False, methods=['DELETE'])
def delete_question_comment(comment_id):
    """Delete the comment with id <comment_id>"""
    comment_id = str(comment_id)
    comment = storage.get(QueComment, comment_id)
    if not comment:
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
    if credential_user.id != comment.user_id:
        abort(401)
    storage.delete(comment)
    return make_response(jsonify({}), 200)


@app_views.route("/comments/answers/<uuid:answer_id>", strict_slashes=False, methods=['POST'])
def new_answer_comment(answer_id):
    """Add a comment for the answer with id <answer_id>"""
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
    a_comment = AnsComment(user_id=credential_user.id, answer_id=answer_id, body=body)
    storage.add(a_comment)
    storage.save()
    return make_response(jsonify(a_comment.to_dict()), 201)

@app_views.route("/comments/answers/<uuid:comment_id>", strict_slashes=False, methods=['PUT'])
def update_answer_comment(comment_id):
    """Update the answer comment with the id <comment_id>"""
    comment_id = str(comment_id)
    comment = storage.get(AnsComment, comment_id)
    if not comment:
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
    if credential_user.id != comment.user_id:
        abort(401)
    comment.update(body=body)
    return make_response(jsonify(comment.to_dict()), 200)


@app_views.route("/comments/answers/<uuid:comment_id>", strict_slashes=False, methods=['DELETE'])
def delete_answer_comment(comment_id):
    """Delete the comment with id <comment_id>"""
    comment_id = str(comment_id)
    comment = storage.get(AnsComment, comment_id)
    if not comment:
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
    if credential_user.id != comment.user_id:
        abort(401)
    storage.delete(comment)
    return make_response(jsonify({}), 200)