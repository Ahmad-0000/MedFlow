#!/usr/bin/python3
"""
Contains main class to manage storage
"""
from os import getenv
from hashlib import md5
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.question import Question
from models.answer import Answer
from models.comments import QueComment, AnsComment
from models.base_model import Base


class Storage():
    """Main class to manage storage"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the main storage object"""
        user = getenv('MEDFLOW_DB_USER')
        pwd = getenv('MEDFLOW_USER_PASSWD')
        host = getenv('MEDFLOW_DB_HOST')
        db = getenv('MEDFLOW_DB')
        url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(user, pwd, host, db)
        Storage.__engine = create_engine(url, pool_pre_ping=True)
        Base.metadata.create_all(Storage.__engine)

    def reload(self):
        """Reload objects from the datebase"""
        Session = scoped_session(sessionmaker(bind=Storage.__engine,
                                              expire_on_commit=False))
        Storage.__session = Session()

    def all(self, cls_list):
        """Retrieve all instances on all classes of cls_list from db"""
        all_obj = {}
        for cls in cls_list:
            all_obj[cls.__name__.lower() + "s"] = Storage.__session.\
                                                  query(cls).all()
        return all_obj

    def some(self, cls, index):
        """Get 5 instances of cls based on after"""
        all_obj = Storage.__session.query(cls).\
            order_by(text("created_at DESC")).all()
        some = []
        if len(all_obj) - 1 < index:
            return some
        for i in range(5):
            some.append(all_obj[index])
            index += 1
            if index > len(all_obj) - 1:
                break
        return some

    def add(self, obj):
        """Add obj to the current session"""
        Storage.__session.add(obj)

    def save(self):
        """Save objects to the database"""
        Storage.__session.commit()

    def delete(self, obj):
        """Delete object from the database"""
        Storage.__session.delete(obj)
        Storage.__session.commit()

    def count(self, cls):
        """Count objects of a given class"""
        objects_list = Storage.__session.query(cls).all()
        return len(objects_list)

    def get(self, cls, id):
        """Get object of a given class based on id"""
        obj = Storage.__session.query(cls).filter_by(id=id).one_or_none()
        return obj

    def close(self):
        """Close the current session"""
        Storage.__session.close()

    def check_user(self, email, password, status="r"):
        """Check if the user with <email> or <password> exists"""
        if status == "r":
            bpassword = password.encode()
            m = md5()
            m.update(bpassword)
            password = m.hexdigest()
        user = Storage.__session.query(User).filter_by(email=email).\
            one_or_none()
        if user:
            return user
        user = Storage.__session.query(User).filter_by(password=password).\
            one_or_none()
        if user:
            return user
        return False

    def credential_user(self, email, password, status="r"):
        """Check if the user with the email <email> and password
        <password> exists
        """
        if status == "r":
            bpassword = password.encode()
            m = md5()
            m.update(bpassword)
            password = m.hexdigest()
        return Storage.__session.query(User).filter_by(email=email).\
               filter_by(password=password).one_or_none()

    def question_fts(self, sentence):
        """Perform fts against questions table using <sentence>"""
        return Storage.__session.query(Question).\
            from_statement(
            text('''SELECT * FROM questions
                 WHERE MATCH (title, body) AGAINST (":sentence")'''))\
            .params(sentence=sentence).all()