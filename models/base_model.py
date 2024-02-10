#!/usr/bin/python3
"""
Custom base class for the entire project
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    That defines:
        all common attributes/methods for other classes
    """

    def __init__(self, *args, **kwargs):
        """
        re-create an instance:
            with this dictionary representation.
        """
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

    def save(self):
        """
        pdates the public instance attribute
        with the current datetime updated_at
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def zh_to_dict(self):
        """
        returns a dictionary containing all keys/values
        of __dict__
        """
        dictReturn = {**self.__dict__}
        dictReturn["__class__"] = type(self).__name__
        dictReturn['created_at'] = dictReturn['created_at'].isoformat()
        dictReturn['updated_at'] = dictReturn['updated_at'].isoformat()

        return(dictReturn)

    def __str__(self):
        """
        That return:
            [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)
