#!/usr/bin/python3
"""Unit tests for the `review` module.
"""
import os
import unittest
from models.review import Review
from models import storage
from datetime import datetime
from models.engine.file_storage import FileStorage

rev1 = Review()
rev2 = Review(**rev1.to_dict())


class TestReview(unittest.TestCase):
    """Test cases for the `Review` class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_attributes(self):
        """Test method for class attributes"""

        key = f"{type(rev1).__name__}.{rev1.id}"
        self.assertIsInstance(rev1.text, str)
        self.assertIsInstance(rev1.user_id, str)
        self.assertIsInstance(rev1.place_id, str)

    def test_init(self):
        """Test method for public instances"""
        self.assertIsInstance(rev1.id, str)
        self.assertIsInstance(rev1.created_at, datetime)
        self.assertIsInstance(rev1.updated_at, datetime)
        self.assertEqual(rev1.updated_at, rev2.updated_at)

    def test_str(self):
        """Test method for str representation"""
        _str = f"[{type(rev1).__name__}] ({rev1.id}) {rev1.__dict__}"
        self.assertEqual(rev1.__str__(), _str)

    def test_save(self):
        """Test method for save"""
        old_update = rev1.updated_at
        rev1.save()
        self.assertNotEqual(rev1.updated_at, old_update)

    def test_todict(self):
        """Test method for dict"""
        r_dict = rev2.to_dict()
        self.assertIsInstance(r_dict, dict)
        self.assertEqual(r_dict['__class__'], type(rev2).__name__)
        self.assertIn('created_at', r_dict.keys())
        self.assertIn('updated_at', r_dict.keys())
        self.assertNotEqual(rev1, rev2)


if __name__ == "__main__":
    unittest.main()
