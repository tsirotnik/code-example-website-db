"""
object mapping to the owner table
"""

from nover.data_access.table import Table


class Owner(Table):
    """
    object mapping to the owner table
    """

    def __init__(self, id=None):
        """
        constructor

        args:
             id : None if new record / row id for record
        """
        self.id = id
        self.image = None
        self.name = None
        self.phone_number = None
        self.email = None
        super(Owner, self).__init__(id)
