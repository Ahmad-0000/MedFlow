from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.answer import Answer
from models.comments import AnsComment
from web_flask.app import flask_app, cache_id


@flask_app.route("/medflow/add_answer_comment/<uuid:a_id>", strict_slashes=False, methods=['GET'])
def add_answer_comment(a_id):
    """Render the template for adding answer comments"""
    return render_template("add_answer_comment.html", a_id=a_id)

@flask_app.route("/medflow/add_answer_comment_handler/<uuid:a_id>", strict_slashes=False, methods=['POST'])
def add_answer_comment_handler(a_id):
    """Adding answer comments"""
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
    body = request.form['body']
    comment = AnsComment(body=body, user_id=user_id, answer_id=answer.id)
    storage.add(comment)
    storage.save()
    return redirect(url_for('get_question', question_id=answer.question_id))


@flask_app.route("/medflow/answers/<uuid:a_id>/update_comment/<uuid:c_id>", strict_slashes=False, methods=['GET'])
def update_answer_comment(a_id, c_id):
    """Render the template update_acomment.html"""
    return render_template("update_acomment.html", a_id=a_id, c_id=c_id)


@flask_app.route("/medflow/answers/<uuid:a_id>/update_comment_handler/<uuid:c_id>", strict_slashes=False, methods=['POST'])
def update_acomment_handler(a_id, c_id):
    """Update the answer comment"""
    a_id = str(a_id)
    c_id = str(c_id)
    a = storage.get(Answer, a_id)
    c = storage.get(AnsComment, c_id)
    if not a or not c:
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
    if user_id != c.user_id:
        abort(401)
    body = request.form.get('body', {})
    if body:
        c.update(body=body)
    return redirect(url_for('get_question', question_id=a.question_id))


@flask_app.route("/medflow/del_acomment/<uuid:c_id>", strict_slashes=False, methods=['POST'])
def del_acomment(c_id):
    """Deletes answer comment with id <c_id>"""
    c_id = str(c_id)
    comment = storage.get(AnsComment, c_id)
    if not comment:
        abort(404)
    status = request.cookies.get("status", None)
    user_id = request.cookies.get("id", None)
    email = request.cookies.get("email", None)
    password = request.cookies.get("password", None)
    if not status or status == "out":
        return make_response(render_template('logfirst.html'), 403)
    if not user_id or not email or not password:
        print("IN Here")
        return make_response(render_template('regfirst.html'), 403)
    id_user = storage.get(User, user_id)
    credentail_user = storage.check_user(email, password, "h")
    if not id_user or not credentail_user:
        return make_response(render_template('regfirst.html'), 403)
    if id_user.to_dict() != credentail_user.to_dict():
        return make_response(render_template("userconflict.html"), 409)
    if comment.user_id != user_id:
        abort(401)
    q_id = comment.answer.question_id
    print(q_id)
    return redirect(url_for('get_question', question_id=q_id))
