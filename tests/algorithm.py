"""
tests search algorithm
"""

import unittest2
from example.tables.owner import Owner
from example.tables.sitter import Sitter
from example.tables.stay import Stay


class Test_Algorithm(unittest2.TestCase):
    """
    tests search algorithm
    """

    def setUp(self):
        """
        setup search algorithm
        """

        # accumulate ids here for deleting after test
        self.owner_ids = []
        self.sitter_ids = []
        self.stay_ids = []

    def test_algo(self):

        test_values = {0: 2.5,
                       1: 2.75,
                       2: 3.00,
                       3: 3.25,
                       4: 3.50,
                       5: 3.75,
                       6: 4.00,
                       7: 4.25,
                       8: 4.50,
                       9: 4.75,
                       10: 5.00,
                       11: 5.00,
                       12: 5.00}

        # create owner
        owner = Owner()
        owner.id = None
        owner.image = "owner image"
        owner.name = "owner name"
        owner.phone_number = "555-555-5555"
        owner.email = "owner@gmail.com"
        owner.save()
        self.owner_ids.append(owner.id)

        # create sitter
        sitter = Sitter()
        sitter.id = None
        sitter.image = "imagename"
        sitter.name = "name"
        sitter.phone = "204-555-5555"
        sitter.email = "dog@gmail.com"
        sitter.ratings_score = 0
        sitter.overall_rank = 0
        sitter.score = 2.5
        sitter.save()
        self.sitter_ids.append(sitter.id)

        # test for zero stays
        assert sitter.refresh().overall_rank == test_values[0]

        # create stay checking each one against the verification table
        for idx in range(1, 13):
            stay = Stay()
            stay.id = None
            stay.review = "review test"
            stay.start_date = "20180101"
            stay.end_date = "20180202"
            stay.rating = 5
            stay.owner_id = owner.id
            stay.sitter_id = sitter.id
            stay.save()
            self.stay_ids.append(stay.id)
            assert sitter.refresh().overall_rank == test_values[idx]

    def tearDown(self):
        """
        tearDown after testing
        """

        # remove the ids that were created during this test
        [Owner(id).delete() for id in self.owner_ids]
        [Sitter(id).delete() for id in self.sitter_ids]
        [Stay(id).delete() for id in self.stay_ids]


if __name__ == "__main__":
    unittest2.main()
