"""
Handle /api/v1/answers endpoint
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.answer import Answer


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
    if "body" not in data or "question_id" not in data or "user_id" not in data:
        abort(400, "Missing data")
    answer = Answer(**data)
    storage.add(answer)
    storage.save()
    return make_response(jsonify(answer.to_dict()), 201)

@app_views.route("/answers/<uuid:answer_id>", strict_slashes=False, methods=['DELETE'])
def delete_answer(answer_id):
    """Delete answer with id <answer_id>"""
    answer_id = str(answer_id)
    answer = storage.get(Answer, answer_id)
    if not answer:
        abort(404)
    storage.delete(answer)
    return make_response(jsonify({}), 200)

@app_views.route("/answers/<uuid:answer_id>", strict_slashes=False, methods=['PUT'])
def update_answer(answer_id):
    """Update answer with id <answer_id>"""
    if not request.is_json:
        abort(400, "Not a JSON")
    answer_id = str(answer_id)
    answer = storage.get(Answer, answer_id)
    if not answer:
        abort(404)
    allowed = ["body", "votes"]
    data = request.get_json()
    filtered_data = {}
    for k, v in data.items():
        if k not in allowed:
            pass
        else:
            filtered_data[k] = v
    answer.update(**filtered_data)
    return make_response(jsonify(answer.to_dict()), 200)
