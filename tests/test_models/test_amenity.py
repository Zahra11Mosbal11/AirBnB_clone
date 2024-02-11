#!/usr/bin/python3
"""Unit tests for the `amenity` module.
"""
import os
import unittest
from models import storage
from datetime import datetime
from models.amenity import Amenity
from models.engine.file_storage import FileStorage

amen1 = Amenity()
amen2 = Amenity(**amen1.to_dict())


class TestAmenity(unittest.TestCase):
    """Test cases for the `Amenity` class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_attributes(self):
        """Test method for class attributes"""

        key = f"{type(amen1).__name__}.{amen1.id}"
        self.assertIsInstance(amen1.name, str)

    def test_init(self):
        """Test method for public instances"""
        self.assertIsInstance(amen1.id, str)
        self.assertIsInstance(amen1.created_at, datetime)
        self.assertIsInstance(amen1.updated_at, datetime)
        self.assertEqual(amen1.updated_at, amen2.updated_at)

    def test_str(self):
        """Test method for str representation"""
        _str = f"[{type(amen1).__name__}] ({amen1.id}) {amen1.__dict__}"
        self.assertEqual(amen1.__str__(), _str)

    def test_save(self):
        """Test method for save"""
        old_update = amen1.updated_at
        amen1.save()
        self.assertNotEqual(amen1.updated_at, old_update)

    def test_todict(self):
        """Test method for dict"""
        a_dict = amen2.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertEqual(a_dict['__class__'], type(amen2).__name__)
        self.assertIn('created_at', a_dict.keys())
        self.assertIn('updated_at', a_dict.keys())
        self.assertNotEqual(amen1, amen2)


if __name__ == "__main__":
    unittest.main()
