from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.question import Question
from web_flask.app import flask_app, cache_id, is_authenticated


@flask_app.route("/medflow/questions/<int:index>")
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


@flask_app.route("/medflow/questions/<uuid:question_id>", strict_slashes=False)
def get_question(question_id):
    """Get one question based on <question_id>"""
    question_id = str(question_id)
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    return render_template('question.html', id=question_id, cache_id=cache_id, status=status, user_id=user_id)

@flask_app.route("/medflow/questions", strict_slashes=False, methods=['GET'])
def questions_page():
    """Render questions template"""
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    return render_template("questions.html", user_id=user_id, cache_id=cache_id, status=status)

@flask_app.route("/medflow/ask", strict_slashes=False, methods=['GET'])
def new_question():
    """Render asking template"""
    status = request.cookies.get("status", None)
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    user_id = request.cookies.get("id", None)
    email = request.cookies.get('email', None)
    password = request.cookies.get('password', None)
    credentail_user = storage.check_user(email, password, "h")
    real_user = storage.get(User, user_id)
    if not credentail_user or not real_user:
        return make_response(render_template('regfirst.html'), 403)
    return render_template('ask.html')

@flask_app.route('/medflow/create_question', strict_slashes=False, methods=['POST'])
def create_question():
    """Create a new question"""
    user_id = request.cookies.get("id", None)
    if not user_id:
        return make_response(render_template('regfirst.html'), 403)
    user_with_id = storage.get(User, user_id)
    if not user_with_id:
        return make_response(render_template('regfirst.html'), 403)
    validation = is_authenticated(user_with_id, request)
    if validation == True:
        data = request.form 
        question = Question(**data, user_id=user_id, votes=0)
        storage.add(question)
        storage.save()
        return redirect(url_for('get_question', question_id=question.id))
    elif validation[1] == 0:
        return make_response(render_template('regfirst.html'), 403)
    elif validation[1] == 1:
        return make_response(render_template('userconfilict.html'), 409)
    else:
        return make_response(render_template('logfirst.html'), 409)

@flask_app.route("/medflow/update_question/<uuid:question_id>", strict_slashes=False, methods=['GET'])
def update_question(question_id):
    """Render update question page"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    status = request.cookies.get("status", None)
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    id = request.cookies.get("id", None)
    id_user = storage.get(User, id)
    if not id_user:
        abort(404)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    if not email or not password:
        return make_response(render_template('regfirst.html'), 403)
    credentail_user = storage.check_user(email, password, "h")
    if credentail_user.to_dict() != id_user.to_dict():
        return make_response(render_template("userconflict.html"), 409)
    if question.user_id != id_user.id:
        abort(401)
    return render_template("update_question.html", question=question)


@flask_app.route("/medflow/update_question_handler/<uuid:question_id>", methods=['POST'], strict_slashes=False)
def update_question_handler(question_id):
    """Update the question with id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    id_user = None
    credentail_user = None
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    if not user_id or not email or not password:
        return make_response(render_template('regfirst.html'), 403)
    id_user = storage.get(User, user_id)
    credentail_user = storage.check_user(email, password, "h")
    if not id_user or not credentail_user:
        abort(404)
    if id_user.to_dict() != credentail_user.to_dict():
        return make_response(render_template("userconflict.html"), 409)
    if question.user_id != user_id:
        abort(401)
    data = request.form
    allowed = ['body', 'title']
    filtered_data = {}
    for k, v in data.items():
        if k not in allowed:
            pass
        else:
            filtered_data[k] = v
    question.update(**filtered_data)
    return redirect(url_for('get_question', question_id=question_id))



@flask_app.route("/medflow/del_question/<uuid:q_id>", strict_slashes=False, methods=['POST'])
def delete_question(q_id):
    """Delete question with id <q_id>"""
    q_id = str(q_id)
    q = storage.get(Question, q_id)
    if not q:
        abort(404)
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    id_user = None
    credentail_user = None
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    if not user_id or not email or not password:
        return make_response(render_template('regfirst.html'), 403)
    id_user = storage.get(User, user_id)
    credentail_user = storage.check_user(email, password, "h")
    if not id_user or not credentail_user:
        abort(404)
    if id_user.to_dict() != credentail_user.to_dict():
        return make_response(render_template("userconflict.html"), 409)
    if q.user_id != user_id:
        abort(401)
    storage.delete(q)
    print(status)
    return redirect(url_for('questions_page'))
