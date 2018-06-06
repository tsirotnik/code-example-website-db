"""
abstract base class for all the selects used to populate web page
"""

from abc import ABCMeta
from example.data_access.database import Database


class View(Database):
    """
    abstract base class for database selects from views
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """
        constructor

        args: --
        """

        # columns are the database columns for the table we want to retrieve
        self.columns = []

        # tablename is derived from class name
        self._tablename = self.__class__.__name__.lower()
        super(View, self).__init__()

    def select(self, clause=""):
        """
        returns the records from the database

        args:
            clause:  this is the database clause that we will append to
                     the end of the select statement
        returns:
            list of database records as ordereddicts

        """
        query = "select {} from {} {}".format(
            ",".join(self.columns), self._tablename, clause)
        data = [r for r in self._db.query(query)]
        return data

    def count(self, clause=""):
        """
        returns the count of the table

        args:
            clause: this is the database clause that we will append to
                    the end of the select statement

        returns:
            count as int

        """
        data = self._db.query(
            "select count(*) from {} {}".format(self._tablename, clause))
        return data.next()['count(*)']


if __name__ == "__main__":
    pass
