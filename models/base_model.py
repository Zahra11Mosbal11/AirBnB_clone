#!/usr/bin/python3
"""
Custom base class for the entire project
"""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """That defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """re-create an instance with this dictionary representation."""
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            return

        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        models.storage.new(self)

    def __str__(self):
        """That return [<class name>] (<self.id>) <self.__dict__>"""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def save(self):
        """pdates the public instance attribute updated_at"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ returns a dictionary containing all keys/values of __dict__"""
        diction = {**self.__dict__}
        diction['__class__'] = type(self).__name__
        diction['created_at'] = diction['created_at'].isoformat()
        diction['updated_at'] = diction['updated_at'].isoformat()

        return diction
