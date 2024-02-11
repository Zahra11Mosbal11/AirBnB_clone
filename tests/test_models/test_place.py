#!/usr/bin/python3
"""Unit tests for the `city` module.
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.place import Place
from models import storage
from datetime import datetime

plc1 = Place()
plc2 = Place(**plc1.to_dict())


class TestPlace(unittest.TestCase):
    """Test cases for the `Place` class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_attributes(self):
        """Test method for class attributes"""

        key = f"{type(plc1).__name__}.{plc1.id}"
        self.assertIn(key, storage.all())
        self.assertIsInstance(plc1.name, str)
        self.assertIsInstance(plc1.user_id, str)
        self.assertIsInstance(plc1.city_id, str)
        self.assertIsInstance(plc1.description, str)
        self.assertIsInstance(plc1.number_bathrooms, int)
        self.assertIsInstance(plc1.number_rooms, int)
        self.assertIsInstance(plc1.price_by_night, int)
        self.assertIsInstance(plc1.max_guest, int)
        self.assertIsInstance(plc1.longitude, float)
        self.assertIsInstance(plc1.latitude, float)
        self.assertIsInstance(plc1.amenity_ids, list)

    def test_init(self):
        """Test method for public instances"""
        self.assertIsInstance(plc1.id, str)
        self.assertIsInstance(plc1.created_at, datetime)
        self.assertIsInstance(plc1.updated_at, datetime)
        self.assertEqual(plc1.updated_at, plc2.updated_at)

    def test_str(self):
        """Test method for str representation"""
        _str = f"[{type(plc1).__name__}] ({plc1.id}) {plc1.__dict__}"
        self.assertEqual(plc1.__str__(), _str)

    def test_save(self):
        """Test method for save"""
        old_update = plc1.updated_at
        plc1.save()
        self.assertNotEqual(plc1.updated_at, old_update)

    def test_todict(self):
        """Test method for dict"""
        p_dict = plc2.to_dict()
        self.assertIsInstance(p_dict, dict)
        self.assertEqual(p_dict['__class__'], type(plc2).__name__)
        self.assertIn('created_at', p_dict.keys())
        self.assertIn('updated_at', p_dict.keys())
        self.assertNotEqual(plc1, plc2)


if __name__ == "__main__":
    unittest.main()
