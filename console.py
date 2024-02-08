#!/usr/bin/python3
"""This module defines the entry point of the command interpreter."""
import cmd
import json
from models import storage
from models.base_model import BaseModel

my_classes = {'BaseModel': BaseModel}


class HBNBCommand(cmd.Cmd):
    """This class represents the command interpreter, and the control center
    of this project.
    """
    prompt = '(hbnb) '

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

        if args[0] not in my_classes.keys():
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

        if args[0] not in my_classes.keys():
            print("** class doesn't exist **")
        if len(args) < 2:
            print("** instance id missing **")
        else:
            instance_id = args[1]
            instance = args[0](instance_id)
            if instance:
                print(instance)
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in my_classes.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")

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

            

if __name__ == "__main__":
    HBNBCommand().cmdloop()
