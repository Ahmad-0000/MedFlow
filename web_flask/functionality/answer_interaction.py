"""
Handles user-answer interaction functionality
"""
from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.question import Question
from models.answer import Answer
from web_flask.app import flask_app, cache_id, is_authenticated, is_item_owner

@flask_app.route("/medflow/answer/<uuid:q_id>", strict_slashes=False, methods=['GET'])
def answer(q_id):
    """Render the template answer.html"""
    q_id = str(q_id)
    return render_template("answer.html", q_id=q_id, cache_id=cache_id)

@flask_app.route("/medflow/answer_question/<uuid:q_id>", strict_slashes=False, methods=['POST'])
def answer_question_handler(q_id):
    """Adds a question answer"""
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
        answer = Answer(user_id=user_id, question_id=q_id, body=request.form['body'])
        storage.add(answer)
        storage.save()
        return redirect(url_for('get_question', question_id=q_id))
    abort(auth_status[1], auth_status[2])


@flask_app.route("/medflow/update_answer/<uuid:answer_id>", strict_slashes=False, methods=['GET'])
def update_answer(answer_id):
    """Render the template update_answer.html"""
    return render_template('update_answer.html', answer_id=answer_id, cache_id=cache_id)

@flask_app.route("/medflow/update_answer_handler/<uuid:a_id>", strict_slashes=False, methods=['POST'])
def update_answer_handler(a_id):
    """Update the answer"""
    a_id = str(a_id)
    answer = storage.get(Answer, a_id)
    if not answer:
        abort(404)
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        if is_item_owner(answer, id_user):
            body = request.form.get("body", {})
            answer.update(body=body)
            return redirect(url_for('get_question', question_id=answer.question_id))
        abort(401)
    abort(auth_status[1], auth_status[2])

@flask_app.route("/medflow/del_answer/<uuid:a_id>", strict_slashes=False, methods=['POST'])
def del_answer(a_id):
    """Delete the answer with the id <a_id>"""
    a_id = str(a_id)
    answer = storage.get(Answer, a_id)
    if not answer:
        abort(404)
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        if is_item_owner(answer, id_user):
            question_id = answer.question_id
            storage.delete(answer)
            return redirect(url_for('get_question', question_id=question_id))
        abort(401)
    abort(auth_status[1], auth_status[2])