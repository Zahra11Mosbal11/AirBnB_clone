#!/usr/bin/python3
"""Unit tests for the `state` module.
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.state import State
from models import storage
from datetime import datetime

sta1 = State()
sta2 = State(**sta1.to_dict())


class TestState(unittest.TestCase):
    """Test cases for the `State` class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_attributes(self):

        key = f"{type(sta1).__name__}.{sta1.id}"
        self.assertIsInstance(sta1.name, str)
        sta1.name = "Chicago"
        self.assertEqual(sta1.name, "Chicago")

    def test_init(self):
        """Test method for public instances"""
        self.assertIsInstance(sta1.id, str)
        self.assertIsInstance(sta1.created_at, datetime)
        self.assertIsInstance(sta1.updated_at, datetime)
        self.assertEqual(sta1.updated_at, sta2.updated_at)

    def test_str(self):
        """Test method for str representation"""
        
        _str = f"[{type(sta1).__name__}] ({sta1.id}) {sta1.__dict__}"
        self.assertEqual(sta1.__str__(), _str)

    def test_save(self):
        """Test method for save"""
        old_update = sta1.updated_at
        sta1.save()
        self.assertNotEqual(sta1.updated_at, old_update)

    def test_todict(self):
        """Test method for dict"""
        s_dict = sta2.to_dict()
        self.assertIsInstance(s_dict, dict)
        self.assertEqual(s_dict['__class__'], type(sta2).__name__)
        self.assertIn('created_at', s_dict.keys())
        self.assertIn('updated_at', s_dict.keys())
        self.assertNotEqual(sta1, sta2)


if __name__ == "__main__":
    unittest.main()
