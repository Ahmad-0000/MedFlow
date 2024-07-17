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
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "body" not in data or "user_id" not in data:
        abort(400, "Missing data")
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    q_comment = QueComment(**data, question_id=question_id)
    storage.add(q_comment)
    storage.save()
    return make_response(jsonify(q_comment.to_dict()), 201)

@app_views.route("/comments/questions/<uuid:comment_id>", strict_slashes=False, methods=['PUT'])
def update_question_comment(comment_id):
    """Update the qustion comment with the id <comment_id>"""
    if not request.is_json:
        abort(400, "Not a JSON")
    comment_id = str(comment_id)
    comment = storage.get(QueComment, comment_id)
    if not comment:
        abort(404)
    data = request.get_json()
    allowed = ["body", "votes"]
    filtered_data = {}
    for k, v in data.items():
        if k not in allowed:
            pass
        else:
            filtered_data[k] = v
    comment.update(**filtered_data)
    return make_response(jsonify(comment.to_dict()), 200)


@app_views.route("/comments/questions/<uuid:comment_id>", strict_slashes=False, methods=['DELETE'])
def delete_question_comment(comment_id):
    """Delete the comment with id <comment_id>"""
    comment_id = str(comment_id)
    comment = storage.get(QueComment, comment_id)
    if not comment:
        abort(404)
    storage.delete(comment)
    return make_response(jsonify({}), 200)








@app_views.route("/comments/answers/<uuid:answer_id>", strict_slashes=False, methods=['POST'])
def new_answer_comment(answer_id):
    """Add a comment for the answer with id <answer_id>"""
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "body" not in data or "user_id" not in data:
        abort(400, "Missing data")
    answer_id = str(answer_id)
    answer = storage.get(Answer, answer_id)
    if not answer:
        abort(404)
    a_comment = AnsComment(**data, answer_id=answer_id)
    storage.add(a_comment)
    storage.save()
    return make_response(jsonify(a_comment.to_dict()), 201)

@app_views.route("/comments/answers/<uuid:comment_id>", strict_slashes=False, methods=['PUT'])
def update_answer_comment(comment_id):
    """Update the answer comment with the id <comment_id>"""
    if not request.is_json:
        abort(400, "Not a JSON")
    comment_id = str(comment_id)
    comment = storage.get(AnsComment, comment_id)
    if not comment:
        abort(404)
    data = request.get_json()
    allowed = ["body", "votes"]
    filtered_data = {}
    for k, v in data.items():
        if k not in allowed:
            pass
        else:
            filtered_data[k] = v
    comment.update(**filtered_data)
    return make_response(jsonify(comment.to_dict()), 200)


@app_views.route("/comments/answers/<uuid:comment_id>", strict_slashes=False, methods=['DELETE'])
def delete_answer_comment(comment_id):
    """Delete the comment with id <comment_id>"""
    comment_id = str(comment_id)
    comment = storage.get(AnsComment, comment_id)
    if not comment:
        abort(404)
    storage.delete(comment)
    return make_response(jsonify({}), 200)