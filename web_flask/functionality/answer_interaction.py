from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.question import Question
from models.answer import Answer
from web_flask.app import flask_app, cache_id

@flask_app.route("/medflow/answer/<uuid:q_id>", strict_slashes=False, methods=['GET'])
def answer(q_id):
    """Render the template answer.html"""
    q_id = str(q_id)
    return render_template("answer.html", q_id=q_id)

@flask_app.route("/medflow/answer_question/<uuid:q_id>", strict_slashes=False, methods=['POST'])
def answer_question(q_id):
    """Adds a question answer"""
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
    answer = Answer(user_id=user_id, question_id=q_id, body=request.form['body'])
    storage.add(answer)
    storage.save()
    return redirect(url_for('get_question', question_id=q_id))


@flask_app.route("/medflow/update_answer/<uuid:answer_id>", strict_slashes=False, methods=['GET'])
def update_answer(answer_id):
    """Render the template update_answer.html"""
    return render_template('update_answer.html', answer_id=answer_id)

@flask_app.route("/medflow/update_answer_handler/<uuid:a_id>", strict_slashes=False, methods=['POST'])
def update_answer_handler(a_id):
    """Update the answer"""
    a_id = str(a_id)
    answer = storage.get(Answer, a_id)
    if not answer:
        abort(404)
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    if not user_id or not email or not password:
        return make_response(render_template('regfirst.html'), 403)
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    id_user = storage.get(User, user_id)
    credentail_user = storage.check_user(email, password, "h")
    if not id_user or not credentail_user:
        return make_response(render_template('regfirst.html'), 403)
    if id_user.to_dict() != credentail_user.to_dict():
        return make_response(render_template("userconflict.html"), 409)
    if answer.user_id != user_id:
        abort(401)
    body = request.form.get("body", {})
    if body:
        answer.update(body=body)
    return redirect(url_for('get_question', question_id=answer.question_id))

@flask_app.route("/medflow/del_answer/<uuid:a_id>", strict_slashes=False, methods=['POST'])
def del_answer(a_id):
    """Delete the answer with the id <a_id>"""
    a_id = str(a_id)
    answer = storage.get(Answer, a_id)
    if not answer:
        abort(404)
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    if not user_id or not email or not password:
        return make_response(render_template('regfirst.html'), 403)
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    id_user = storage.get(User, user_id)
    credentail_user = storage.check_user(email, password, "h")
    if not id_user or not credentail_user:
        return make_response(render_template('regfirst.html'), 403)
    if id_user.to_dict() != credentail_user.to_dict():
        return make_response(render_template("userconflict.html"), 409)
    if answer.user_id != user_id:
        abort(401)
    question_id = answer.question_id
    storage.delete(answer)
    return redirect(url_for('get_question', question_id=question_id))
