"""
Handeling /api/v1/questions endpoint
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views, paginate
from models import storage
from models.question import Question


@app_views.route("/questions/<int:index>")
def some_questions(index):
    """
    Get 5 questions from the database starting from index <index>
    (included)
    """
    questions = storage.some(Question, index)
    questions_repr = []
    for q in questions:
        questions_repr.append(q.to_dict())
    return jsonify(questions_repr)

@app_views.route("/questions/<uuid:question_id>", strict_slashes=False)
def get_question(question_id):
    """Get one question based on <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    return jsonify(question.to_dict())


@app_views.route("/questions/<uuid:question_id>/comments", strict_slashes=False)
def get_question_comments(question_id):
    """Get all question comments of the question with id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    comments = question.comments
    comments_repr = []
    for comment in comments:
        comments_repr.append(comment.to_dict())
    return jsonify(comments_repr)


@app_views.route("/questions/<uuid:question_id>/answers", strict_slashes=False)
def get_question_answers(question_id):
    """Get all question answers of the question with id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    answers = question.answers
    answer_repr = []
    for answer in answers:
        answer_repr.append(answer.to_dict())
    return jsonify(answer_repr)


@app_views.route("/questions", strict_slashes=False, methods=['POST'])
def new_question():
    """Create a new question"""
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    title = data.get("title", None)
    body = data.get("body", None)
    if not email or not password or not title or not body:
        abort(400, "Missing data")
    user = storage.credential_user(email, password)
    if not user:
        abort(400, "Wrong credentials")
    question = Question(user_id=user.id, title=title, body=body)
    storage.add(question)
    storage.save()
    return make_response(jsonify(question.to_dict()), 201)

@app_views.route("/questions/<uuid:question_id>", strict_slashes=False, methods=["PUT"])
def update_question(question_id):
    """Update question with the id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    title = data.get("title", None)
    body = data.get("body", None)
    if not email or not password:
        abort(400, "Missing credentials")
    credential_user = storage.credential_user(email, password)
    if not credential_user:
        abort(400, "Wrong credentials")
    if credential_user.id != question.user_id:
        abort(401)
    if title or body:
        allowed = ["title", "body"]
        filtered_data = {}
        for k, v in data.items():
            if k not in allowed:
                pass
            else:
                filtered_data[k] = v
        question.update(**filtered_data)
        return make_response(jsonify(question.to_dict()), 200)
    abort(400, "Missing data")

@app_views.route("/questions/<uuid:question_id>", strict_slashes=False, methods=["DELETE"])
def remove_question(question_id):
    """Delete question with the id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)
    if not email or not password:
        abort(400, "Missing credentials")
    credential_user = storage.credential_user(email, password)
    if not credential_user:
        abort(400, "Wrong credentials")
    if credential_user.id != question.user_id:
        abort(401)
    storage.delete(question)
    return make_response(jsonify({}), 200)


@app_views.route("/questions_fts", methods=['POST'], strict_slashes=False)
def questions_fts():
    """Conduct a full text on "questions" table"""
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'sentence' not in data:
        abort(400, "Missing sentence")
    if 'index' not in data:
        abort(400, "Missing index")
    index = data['index']
    sentence = data['sentence']
    result = storage.question_fts(sentence)
    some_questions = paginate(result, 5, index)
    questions_repr = []
    for q in some_questions:
        questions_repr.append(q.to_dict())
    return jsonify(questions_repr)