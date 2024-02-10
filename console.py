#!/usr/bin/python3
"""This module defines the entry point of the command interpreter."""
import cmd
import json
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place

my_classes = {'BaseModel': BaseModel, 'User': User,
              'Amenity': Amenity, 'City': City, 'State': State,
              'Place': Place, 'Review': Review}


class HBNBCommand(cmd.Cmd):
    """This class represents the command interpreter, and the control center
    of this project.
    """
    prompt = '(hbnb) '

    def default(self, line):
        """Defines instructions to execute before <line> is interpreted."""
        classes = ["BaseModel", "User", "State", "City", "Amenity",
                                "Place", "Review"]

        com_list = {"all": self.do_all,
                    "count": self.class_count,
                    "show": self.do_show,
                    "destroy": self.do_destroy,
                    "update": self.do_update}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in classes \
                or args[1] not in com_list.keys():
            super().default(line)
            return

        if args[1] in ["all", "count"]:
            com_list[args[1]](args[0])
        elif args[1] in ["show", "destroy"]:
            com_list[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            par = re.match(r"\"(.+?)\", (.+)", args[2])
            if par.groups()[1][0] == '{':
                dic_p = eval(par.groups()[1])
                for key, val in dic_p.items():
                    com_list[args[1]](args[0] + " " + par.groups()[0] +
                                      " " + key + " " + str(val))
            else:
                resalt = par.groups()[1].split(", ")
                com_list[args[1]](args[0] + " " + par.groups()[0] + " " +
                                  resalt[0] + " " + resalt[1])

    def class_count(self, my_class):
        """counts instances of a certain class"""
        count = 0

        for instance_obj in storage.all().values():
            if instance_obj.__class__.__name__ == my_class:
                count += 1
        print(count)

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Inbuilt EOF command to gracefully catch errors."""
        print("")
        return True

    def do_help(self, arg):
        """To get help on a command, type help <topic>."""
        return super().do_help(arg)

    def emptyline(self):
        """Override default `empty line + return` behaviour."""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in my_classes.keys():
            print("** class doesn't exist **")
        else:
            obj_new = my_classes[args[0]]()
            obj_new.save()
            print(obj_new.id)

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in my_classes.keys():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            instanceObjs = storage.all()
            key = "{}.{}".format(args[0], args[1])
            _instance = instanceObjs.get(key, None)
            if _instance is None:
                print("** no instance found **")
                return
            print(_instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in my_classes.keys():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            instanceObjs = storage.all()
            key = "{}.{}".format(args[0], args[1])
            _instance = instanceObjs.get(key, None)
            if _instance is None:
                print("** no instance found **")
                return

            del instanceObjs[key]
            storage.save()

    def do_all(self, arg):
        """Prints string representation of all instances.
        """
        args = arg.split()
        _all = storage.all()

        if len(args) < 1:
            print(["{}".format(str(v)) for _, v in _all.items()])
        elif args[0] not in my_classes.keys():
            print("** class doesn't exist **")
        else:
            print(["{}".format(str(v))
                  for _, v in _all.items() if type(v).__name__ == args[0]])
            return

    def do_update(self, arg):
        """adding or updating attribute
        update <class name> <id> <attribute name> "<attribute value>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in my_classes.keys():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
            return
        instanceObjs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        _instance = instanceObjs.get(key, None)
        if _instance is None:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            match = re.findall(r"{.*}", arg)
            if match:
                _load = None
                try:
                    _load: dict = json.loads(match[0])
                except Exception:
                    print("** invalid syntax")
                    return
                for key, val in _load.items():
                    setattr(_instance, key, val)
                storage.save()
                return
            _attr = re.findall(r"^[\"\'](.*?)[\"\']", args[3])
            if _attr:
                setattr(_instance, args[2], _attr[0])
            else:
                valueList = args[3].split()
                setattr(_instance, args[2], simple_str(valueList[0]))
            storage.save()

    def simple_str(arg):
        """Parse `arg` to an `int`, `float` or `string`."""
        par = re.sub("\"", "", arg)

        if isInt(par):
            return int(par)
        elif isFloat(par):
            return float(par)
        else:
            return arg

    def isFloat(i):
        """Checks if 'x'is float."""
        try:
            a = float(i)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def isInt(i):
        """Checks if `x` is int."""
        try:
            a = float(i)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b


if __name__ == "__main__":
    HBNBCommand().cmdloop()
