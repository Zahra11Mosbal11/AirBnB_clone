#!/usr/bin/python3
"""Defines:
FileStorage class.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class FileStorage:
    """Private class attributes """
    __filePath = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """ serializes __objects to the JSON file """
        dict_Obj = {}

        for key, value in FileStorage.__objects.items():
            dict_Obj[key] = value.zh_to_dict()
            with open(FileStorage.__filePath, "w", encoding="utf-8") as jsonF:
                json.dump(dict_Obj, jsonF)

    def reload(self):
        """ deserializes the JSON file to __objects """
        definedClasses = {'BaseModel': BaseModel, 'User': User,
                          'Amenity': Amenity, 'City': City, 'State': State,
                          'Place': Place, 'Review': Review}
        try:
            with open(FileStorage.__filePath, encoding="utf-8") as jsonStr:
                deser = json.load(jsonStr)
                for obj_values in deser.values():
                    clsName = obj_values["__class__"]
                    cls_obj = definedClasses[clsName]

                    self.new(cls_obj(**obj_values))

        except FileNotFoundError:
            pass
