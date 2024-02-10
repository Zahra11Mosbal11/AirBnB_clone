#!/usr/bin/python3
"""
Module: basemodel.py
"""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """That defines all:
    common attributes/methods for other classes
    """

    def __init__(self, *args, **kwargs):
        """re-create an instance:
        with this dictionary representation.
        """
        if kwargs:
            del kwargs["__class__"]
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    dtime_obj = datetime.fromisoformat(value)
                    setattr(self, key, dtime_obj)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            models.storage.new(self)

    def save(self):
        """pdates the public instance attribute updated_at"""
        self.updated_at = datetime.now()
        models.storage.save()

    def zh_to_dict(self):
        """ returns a dictionary containing all keys/values of __dict__ """
        dictReturn = {}

        dictReturn["__class__"] = self.__class__.__name__

        for key, val in self.__dict__.items():
            if isinstance(val, datetime):
                dictReturn[key] = val.isoformat()
            else:
                dictReturn[key] = val
        return(dictReturn)

    def __str__(self):
        """That return [<class name>] (<self.id>) <self.__dict__>"""
        return f"{[self.__class__.__name__]} {(self.id)} {self.__dict__}"
