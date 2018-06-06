"""
provides database connection
base class for all the data access objects
"""

import dataset

class Database(object):
    """
    provides database connection
    base class for all the database classes
    """
    def __init__(self):
        """
        constructor - sets up the database connection

        args: --
        """
        try:
            self._db = dataset.connect("sqlite:///sqlite_db/example.sqlite")
        except Exception as error:
            print "unable to make database connection"
            raise error
