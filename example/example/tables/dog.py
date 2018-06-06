"""
object mapping to the dog table
"""

from example.data_access.table import Table


class Dog(Table):
    """
    object mapping to the dog table
    """

    def __init__(self, id=None):
        """
        constructor

        args:
             id : None if new record / row id for record
        """
        self.id = id
        self.name = None
        self.owner_id = None
        super(Dog, self).__init__(id)
