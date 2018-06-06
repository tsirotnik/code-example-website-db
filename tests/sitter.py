"""
tests data access to the sitter table
"""

import unittest2
from example.tables.sitter import Sitter


class Test_Sitter(unittest2.TestCase):
    """
    tests data access to the sitter table
    """

    def test_sitter_crud_operations(self):
        """
        subtests
            creating new sitter
            instantiating from existing record
            updating
            delete
        """
        id = None

        with self.subTest("create"):
            sitter = Sitter()
            sitter.id = None
            sitter.image = "imagename"
            sitter.name = "name"
            sitter.phone = "204-555-5555"
            sitter.email = "dog@gmail.com"
            # calculated values tested in algorithm tests
            #sitter.ratings_score = 1.1
            #sitter.score = 2.2
            #sitter.overall_rank = 3.3
            sitter.save()
            assert sitter.id is not None
            id = sitter.id

        with self.subTest("instantiate from id"):
            sitter = Sitter(id)
            assert sitter.id == id
            assert sitter.image == "imagename"
            assert sitter.name == "name"
            assert sitter.phone == "204-555-5555"
            assert sitter.email == "dog@gmail.com"
            # calculated values tested in algorithm tests
            #assert sitter.ratings_score == 1.1
            #assert sitter.score == 2.2
            #assert sitter.overall_rank == 3.3

        with self.subTest("update"):
            sitter = Sitter(id)
            sitter.image = "imagename - updated"
            sitter.name = "name - updated"
            sitter.phone = "204-555-5555 - updated"
            sitter.email = "dog@gmail.com - updated"
            # calculated values tested in algorithm tests
            #sitter.ratings_score = 8.8
            #sitter.score = 7.7
            #sitter.overall_rank = 6.6
            sitter.save()

            del sitter

            sitter2 = Sitter(id)
            assert sitter2.image == "imagename - updated"
            assert sitter2.name == "name - updated"
            assert sitter2.phone == "204-555-5555 - updated"
            assert sitter2.email == "dog@gmail.com - updated"
            # calculated values tested in algorithm tests
            #assert sitter2.ratings_score == 8.8
            #assert sitter2.score == 7.7
            #assert sitter2.overall_rank == 6.6

        with self.subTest("delete"):
            sitter = Sitter(id)
            sitter.delete()


if __name__ == "__main__":

    unittest2.main()
