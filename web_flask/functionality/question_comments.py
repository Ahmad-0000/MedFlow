from flask import make_response, request, redirect, render_template, abort, url_for
from models import storage
from models.user import User
from models.question import Question
from models.comments import QueComment
from web_flask.app import flask_app, cache_id



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
    return redirect(url_for('get_question', question_id=q_id))

    
@flask_app.route("/medflow/del_qcomment/<uuid:c_id>", strict_slashes=False, methods=['POST'])
def del_qcomment(c_id):
    """Deletes question comment with id <q_comment>"""
    c_id = str(c_id)
    comment = storage.get(QueComment, c_id)
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
    q_id = comment.question_id
    storage.delete(comment)
    return redirect(url_for('get_question', question_id=q_id))

@flask_app.route("/medflow/add_question_comment/<uuid:question_id>", strict_slashes=False)
def add_question_comment(question_id):
    """Renders a page to adding a question comment"""
    return render_template("question_comment.html", id=question_id)

@flask_app.route("/medflow/add_question_comment_handler/<uuid:q_id>", strict_slashes=False, methods=['POST'])
def add_question_comment_handler(q_id):
    """Adds a question comment"""
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
    data = request.form
    com = QueComment(question_id=q.id, user_id=user_id, **data)
    storage.add(com)
    storage.save()
    return redirect(url_for('get_question', question_id=q.id)) 
