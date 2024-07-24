"""
Handles user-questions interaction functionality
"""
from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.question import Question
from web_flask.app import flask_app, cache_id, is_authenticated, is_item_owner, errors



@flask_app.route("/medflow/questions/<uuid:question_id>", strict_slashes=False, methods=['GET'])
def get_question(question_id):
    """Render the page of the question with id <question_id>"""
    question_id = str(question_id)
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
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
    return render_template('ask.html', cache_id=cache_id)

@flask_app.route('/medflow/create_question', strict_slashes=False, methods=['POST'])
def create_question():
    """Create a new question"""
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    user_with_id = storage.get(User, user_id)
    if not user_with_id:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(user_with_id, request)
    if auth_status[0]:
        data = request.form 
        question = Question(**data, user_id=user_id)
        storage.add(question)
        storage.save()
        return redirect(url_for('get_question', question_id=question.id))
    abort(auth_status[1], auth_status[2])

@flask_app.route("/medflow/update_question/<uuid:question_id>", strict_slashes=False, methods=['GET'])
def update_question(question_id):
    """Render update question page"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    return render_template("update_question.html", question=question, cache_id=cache_id)


@flask_app.route("/medflow/update_question_handler/<uuid:question_id>", methods=['POST'], strict_slashes=False)
def update_question_handler(question_id):
    """Update the question with id <question_id>"""
    question_id = str(question_id)
    question = storage.get(Question, question_id)
    if not question:
        abort(404)
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_regiestration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        if is_item_owner(question, id_user):
            data = request.form
            filtered_data = {}
            for k, v in data.items():
                if k == 'body' or k == 'title':
                    filtered_data[k] = v
                else:
                    pass
            question.update(**filtered_data)
            return redirect(url_for('get_question', question_id=question_id))
        abort(401)
    abort(auth_status[1], auth_status[2])



@flask_app.route("/medflow/del_question/<uuid:q_id>", strict_slashes=False, methods=['POST'])
def delete_question(q_id):
    """Delete question with id <q_id>"""
    q_id = str(q_id)
    question = storage.get(Question, q_id)
    if not question:
        abort(404)
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        if is_item_owner(question, id_user):
            storage.delete(question)
            return redirect(url_for('questions_page'))
        abort(401)
    abort(auth_status[1], auth_status[2])