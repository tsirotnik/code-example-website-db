"""
tests data access to the dog table
"""

import unittest2
from example.tables.dog import Dog


class Test_Dog(unittest2.TestCase):
    """
    tests data access to the dog interface
    """

    def test_dog_crud_operations(self):
        """
        subtests
           creating new dog
           instantiating from existing record
           updating
           delete
        """
        id = None

        with self.subTest("create"):
            dog = Dog()
            dog.id = None
            dog.name = "sparky"
            dog.save()
            assert dog.id is not None
            id = dog.id

        with self.subTest("instantiate from id"):
            dog = Dog(id)
            assert dog.id == id
            assert dog.name == "sparky"

        with self.subTest("update"):
            dog = Dog(id)
            dog.name = "sparky - updated"
            dog.save()

            del dog

            dog2 = Dog(id)
            assert dog2.name == "sparky - updated"

        with self.subTest("delete"):
            dog = Dog(id)
            dog.delete()


if __name__ == "__main__":

    unittest2.main()
