"""
object mapping to the sitterlist view
"""

import json
from nover.data_access.view import View


class SitterList(View):
    """
    object mapping to the sitterlist view
    """

    def __init__(self):
        """
        constructor

        sets the columns to return from the select

        args: --
        """
        super(SitterList, self).__init__()
        self.columns = ['Sitter', 'Photo', 'Rating']

    def data(self, begin_index, filterby, limit=10):
        """
        returns sitter information data

        args:
            begin_index: the offset from which to start
                         returning records
            filterby   : the rank to filter by
            limit      :  how many records to return
        """
        try:
            # simple validation, ensure no injection problems
            float(begin_index)
            float(filterby)
        except AssertionError as error:
            print str(error)
            print "arguments incorrect!"
            raise error

        count = self.count("where rating > {}".format(filterby))
        data = self.select("where rating > {} order by rank limit {} offset {}".format(
            filterby, limit, begin_index))

        jsondata = json.dumps({"data": data,
                               "itemsCount": count})

        return jsondata
