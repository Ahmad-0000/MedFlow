"""
Contains main API blueprint
"""
from flask import Blueprint
from models import storage
from models.user import User
from models.question import Question
from models.answer import Answer
from models.comments import AnsComment, QueComment


app_views = Blueprint("app_views", __name__)

@app_views.route("/status", strict_slashes=False)
def api_status():
    """Return api status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def api_stats():
    """Return stats about the website"""
    stats = {
            "users": storage.count(User),
            "questions": storage.count(Question),
            "answers": storage.count(Answer),
            "question comments": storage.count(QueComment),
            "answer comments": storage.count(AnsComment),
        }
    return jsonify(stats)

def paginate(items, limit, index):
    """"""
    some = []
    if len(items) - 1 < index:
        return some
    for i in range(limit):
        some.append(items[index])
        index += 1
        if index > len(items) - 1:
            break
    return some

from api.v1.views.questions import *
from api.v1.views.users import *
from api.v1.views.answers import *
from api.v1.views.comments import *