"""
Handles answer comments-user interaction functionality
"""
from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.answer import Answer
from models.comments import AnsComment
from web_flask.app import flask_app, cache_id, is_authenticated, is_item_owner


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
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        body = request.form['body']
        comment = AnsComment(body=body, user_id=user_id, answer_id=answer.id)
        storage.add(comment)
        storage.save()
        return redirect(url_for('get_question', question_id=answer.question_id))
    abort(auth_status[1], auth_status[2])


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
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        if is_item_owner(c, id_user):
            body = request.form.get('body', {})
            if body:
                c.update(body=body)
            return redirect(url_for('get_question', question_id=a.question_id))
        abort(401)
    abort(auth_status[1], auth_status[2])


@flask_app.route("/medflow/del_acomment/<uuid:c_id>", strict_slashes=False, methods=['POST'])
def del_acomment(c_id):
    """Deletes answer comment with id <c_id>"""
    c_id = str(c_id)
    comment = storage.get(AnsComment, c_id)
    if not comment:
        abort(404)
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        if is_item_owner(comment, id_user):
            q_id = comment.answer.question_id
            storage.delete(comment)
            return redirect(url_for('get_question', question_id=q_id))
        abort(401)
    abort(auth_status[1], auth_status[2])