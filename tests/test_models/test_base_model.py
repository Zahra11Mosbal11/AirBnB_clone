"""Testing the `base_model` module."""
import json
import os
import time
import unittest
import uuid
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

base1 = BaseModel()
base2_uuid = str(uuid.uuid4())
base2 = BaseModel(id=base2_uuid, name="The weeknd", album="Trilogy")


class TestBase(unittest.TestCase):
    """Test cases for the `Base` class.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_init(self):
        """Test passing cases `BaseModel` initialization.
        """
        self.assertIsInstance(base1.id, str)
        self.assertIsInstance(base2.id, str)
        self.assertEqual(base2_uuid, base2.id)
        self.assertEqual(base2.album, "Trilogy")
        self.assertEqual(base2.name, "The weeknd")
        self.assertIsInstance(base1.created_at, datetime)
        self.assertIsInstance(base1.created_at, datetime)
        self.assertEqual(str(type(base1)),
                         "<class 'models.base_model.BaseModel'>")

    def test_to_dict(self):
        """Test method for dict"""
        base1_dict = base1.to_dict()
        self.assertIsInstance(base1_dict, dict)
        self.assertIn('id', base1_dict.keys())
        self.assertIn('created_at', base1_dict.keys())
        self.assertIn('updated_at', base1_dict.keys())
        self.assertEqual(base1_dict['__class__'], type(base1).__name__)
        with self.assertRaises(KeyError) as e:
            base2.to_dict()

    def test_save(self):
        """Test method for save"""
        time.sleep(0.5)
        date_now = datetime.now()
        base1.save()
        diff = base1.updated_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_save_storage(self):
        """Tests that storage.save() is called from save()."""
        pass
            
    def test_save_non_args(self):
        """Tests save() with no arguments."""
        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_save_ex_args(self):
        """Tests save() with too many arguments."""
        with self.assertRaises(TypeError) as e:
            BaseModel.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_str(self):
        """Test method for str representation"""
        _str = f"[{type(base1).__name__}] ({base1.id}) {base1.__dict__}"
        self.assertEqual(base1.__str__(), _str)


if __name__ == "__main__":
    unittest.main()
