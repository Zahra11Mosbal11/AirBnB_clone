#!/usr/bin/python3
from uuid import uuid4
import datetime


class BaseModel:
    """That defines all common attributes/methods for other classes"""
    def __init__(self):
        """Initialize a new Base.
        Args:
            id (int): The identity of the new Base.
        """
        self.id = str(uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def save(self):
        """pdates the public instance attribute updated_at"""
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """ returns a dictionary containing all keys/values of __dict__ """
        dictReturn = {}

        dictReturn["__class__"] = self.__class__.__name__

        for key, val in self.__dict__.items():
            if isinstance(val, datetime.datetime):
                dictReturn[key] = val.isoformat()
            else:
                dictReturn[key] = val
        return(dictReturn)

    def __str__(self):
        """That return [<class name>] (<self.id>) <self.__dict__>"""
        return f"{[self.__class__.__name__]} {(self.id)} {self.__dict__}"

