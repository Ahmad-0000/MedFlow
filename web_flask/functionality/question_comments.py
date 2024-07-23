"""
Handles question comments-user interaction functionality
"""
from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.question import Question
from models.comments import QueComment
from web_flask.app import flask_app, cache_id, is_authenticated, is_item_owner


@flask_app.route("/medflow/add_question_comment/<uuid:question_id>", strict_slashes=False)
def add_question_comment(question_id):
    """Renders a page for adding a question comment"""
    return render_template("question_comment.html", id=question_id)

@flask_app.route("/medflow/add_question_comment_handler/<uuid:q_id>", strict_slashes=False, methods=['POST'])
def add_question_comment_handler(q_id):
    """Adds a question comment"""
    q_id = str(q_id)
    q = storage.get(Question, q_id)
    if not q:
        abort(404)
    user_id = request.cookies.get("id", None)
    if not user_id:
        abort(403, 'err_registeration')
    id_user = storage.get(User, user_id)
    if not id_user:
        abort(403, 'err_registeration')
    auth_status = is_authenticated(id_user, request)
    if auth_status[0]:
        data = request.form
        com = QueComment(question_id=q.id, user_id=user_id, **data)
        storage.add(com)
        storage.save()
        return redirect(url_for('get_question', question_id=q.id))
    abort(auth_status[1], auth_status[2])

@flask_app.route("/medflow/questions/<uuid:q_id>/update_comment/<uuid:c_id>", strict_slashes=False, methods=['GET'])
def update_comment(q_id, c_id):
    """Render the template update_qcomment.html"""
    return render_template("update_qcomment.html", q_id=q_id, c_id=c_id)

@flask_app.route("/medflow/questions/<uuid:q_id>/update_comment_handler/<uuid:c_id>", strict_slashes=False, methods=['POST'])
def update_qcomment_handler(q_id, c_id):
    """Update the question comment"""
    q_id = str(q_id)
    c_id = str(c_id)
    q = storage.get(Question, q_id)
    c = storage.get(QueComment, c_id)
    if not q or not c:
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
            return redirect(url_for('get_question', question_id=q_id))
        abort(401)
    abort(auth_status[1], auth_status[2])

    
@flask_app.route("/medflow/del_qcomment/<uuid:c_id>", strict_slashes=False, methods=['POST'])
def del_qcomment(c_id):
    """Deletes question comment with id <q_comment>"""
    c_id = str(c_id)
    comment = storage.get(QueComment, c_id)
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
            q_id = comment.question_id
            storage.delete(comment)
            return redirect(url_for('get_question', question_id=q_id))
        abort(401)
    abort(auth_status[1], auth_status[2])