#!/usr/bin/python3
"""
Contains the base model that other models will inherit from
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5

Base = declarative_base()


class BaseModel():
    """Base Model that other models will inherit from"""

    id = Column(String(40), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize the object"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            for k, v in kwargs.items():
                if k != "__class__":
                    if k == "created_at" or k == "updated_at":
                        self.__dict__[k] = datetime.fromisoformat(v)
                    if k == "password":
                        m = md5()
                        passwd = kwargs[k]
                        passwd = passwd.encode()
                        m.update(passwd)
                        hashed_passwd = m.hexdigest()
                        self.__dict__[k] = hashed_passwd
                    else:
                        self.__dict__[k] = v
            if "id" not in self.__dict__:
                self.id = str(uuid4())
            if "created_at" not in self.__dict__:
                self.created_at = datetime.utcnow()
            if "updated_at" not in self.__dict__:
                self.updated_at = datetime.utcnow()

    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def update(self, *args, **kwargs):
        """Update the current object"""
        from models import storage
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
            self.updated_at = datetime.utcnow()
            storage.save()

    def to_dict(self):
        """Make dict representation of an object"""
        dict_repr = {}
        for k, v in self.__dict__.items():
            if k == 'created_at' or k == 'updated_at':
                dict_repr[k] = datetime.isoformat(v)
            else:
                dict_repr[k] = v
        dict_repr['__class__'] = self.__class__.__name__
        try:
            del dict_repr['_sa_instance_state']
        except KeyError:
            pass
        return dict_repr

    def delete(self):
        """Delete this object from the database"""
        from models import storage
        storage.delete(self)
