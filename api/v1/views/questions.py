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
        abort(404, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data or "title" not in data or "body" not in data:
        abort(400, "Missing data")
    question = Question(user_id=data['user_id'], title=data["title"],
                        body=data["body"], votes=0)
    storage.add(question)
    storage.save()
    return make_response(jsonify(question.to_dict()), 201)

@app_views.route("/questions/<uuid:question_id>", strict_slashes=False, methods=["DELETE"])
def remove_question(question_id):
    """Delete question with the id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    storage.delete(question)
    return make_response(jsonify({}), 200)

@app_views.route("/questions/<uuid:question_id>", strict_slashes=False, methods=["PUT"])
def update_question(question_id):
    """Update question with the id <question_id>"""
    if not request.is_json:
        abort(400, "Not a JSON")
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    data = request.get_json()
    allowed = ["title", "body", "votes"]
    filtered_data = {}
    for k, v in data.items():
        if k not in allowed:
            pass
        else:
            filtered_data[k] = v
    question.update(**filtered_data)
    return make_response(jsonify(question.to_dict()), 200)


@app_views.route("/questions_fts", methods=['POST'], strict_slashes=False)
def questions_fts():
    """Conduct a full text on "questions" table"""
    if not request.is_json:
        print("Here")
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
