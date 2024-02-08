#!/usr/bin/python3
"""Defines FileStorage class."""
import json
from models.base_model import BaseModel

class FileStorage:
    """ Private class attributes """
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
        try:
            with open(FileStorage.__filePath, encoding-"utf-8") as jsonStr:
                deser = json.load(jsonStr)
                for obj_values in deser.values():
                    clsName = obj_values["__class__"]
                    if isinstance(clsName, str) and type(eval(clsName) == type:
                            self.new(eval(clsName)(**obj_values))
        except FileNOtFoundError:
        pass
