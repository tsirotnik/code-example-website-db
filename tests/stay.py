"""
tests data access to the stay table
"""


import unittest2
from example.tables.stay import Stay


class Test_Stay(unittest2.TestCase):
    """
    tests data access to the stay table
    """

    def test_stay_crud_operations(self):
        """
        subtests
            creating new stay
            instantiating from existing record
            updating
            deleting
        """

        id = None

        with self.subTest("create"):
            stay = Stay()
            stay.id = None
            stay.review = "review test"
            stay.start_date = "20180101"
            stay.end_date = "20180202"
            stay.rating = 5
            stay.save()
            assert stay.id is not None
            id = stay.id

        with self.subTest("instantiate from id"):
            stay = Stay(id)
            assert stay.id == id
            assert stay.review == "review test"
            assert stay.start_date == "20180101"
            assert stay.end_date == "20180202"
            assert stay.rating == 5

        with self.subTest("update"):
            stay = Stay(id)
            stay.review = "review test - updated"
            stay.start_date = "20180101 - updated"
            stay.end_date = "20180202 - updated"
            stay.rating = 0
            stay.save()

            del stay

            stay2 = Stay(id)
            assert stay2.review == "review test - updated"
            assert stay2.start_date == "20180101 - updated"
            assert stay2.end_date == "20180202 - updated"
            assert stay2.rating == 0

        with self.subTest("delete"):
            stay = Stay(id)
            stay.delete()


if __name__ == "__main__":

    unittest2.main()
