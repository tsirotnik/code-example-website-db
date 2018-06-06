"""
tests data access to the owner table
"""
import unittest2
from example.tables.owner import Owner


class Test_Owner(unittest2.TestCase):
    """
    tests data access to the owner table
    """

    def test_owner_crud_operations(self):
        """
        subtests
            creating new owner
            instantiating from existing record
            updating
            delete
        """
        id = None

        with self.subTest("create"):
            owner = Owner()
            owner.id = None
            owner.image = "owner image"
            owner.name = "owner name"
            owner.phone_number = "555-555-5555"
            owner.email = "owner@gmail.com"
            owner.save()
            assert owner.id is not None
            id = owner.id

        with self.subTest("instantiate from id"):
            owner = Owner(id)
            assert owner.id == id
            assert owner.image == "owner image"
            assert owner.name == "owner name"
            assert owner.phone_number == "555-555-5555"
            assert owner.email == "owner@gmail.com"

        with self.subTest("update"):
            owner = Owner(id)
            owner.image = "owner image - updated"
            owner.name = "owner name - updated"
            owner.phone_number = "555-555-5555 - updated"
            owner.email = "owner@gmail.com - updated"
            owner.save()
            del owner

            owner2 = Owner(id)
            assert owner2.image == "owner image - updated"
            assert owner2.name == "owner name - updated"
            assert owner2.phone_number == "555-555-5555 - updated"
            assert owner2.email == "owner@gmail.com - updated"

        with self.subTest("delete"):
            owner = Owner(id)
            owner.delete()


if __name__ == "__main__":

    unittest2.main()
