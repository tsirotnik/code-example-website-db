"""
tests data access to the owner table
"""
import json
import unittest2
from example.tables.sitter_list import SitterList
from example.data_access.database import Database

class Test_SitterList(unittest2.TestCase):
    """
    tests data access to SitterList view
    """
    def test_get_data(self):
        sitterlist = SitterList()
        json_data = sitterlist.data(0,0,10)

        data = json.loads(json_data)

        result = Database()._db.query("select count(*) from sitterlist");
        count = result.next()['count(*)']

        assert data['itemsCount'] == count
        assert len(data['data']) == 10

    def test_rating_filter(self):
        sitterlist = SitterList()
        json_data = sitterlist.data(0,4,10)

        data = json.loads(json_data)

        for record in data['data']:
            assert record['Rating'] > 4

        json_data = sitterlist.data(0,2,10)

        data = json.loads(json_data)

        for record in data['data']:
            assert record['Rating'] > 2

    def test_record_limit(self):
        sitterlist = SitterList()

        json_data = sitterlist.data(0,0,6)
        data = json.loads(json_data)
        assert len(data['data']) == 6

        json_data = sitterlist.data(0,0,4)
        data = json.loads(json_data)
        assert len(data['data']) == 4

if __name__ == "__main__":

    unittest2.main()
