"""
object mapping to the stay table
"""
from nover.data_access.table import Table


class Stay(Table):
    """
    object mapping to the stay table
    """

    def __init__(self, id=None):
        self.id = id
        self.review = None
        self.start_date = None
        self.end_date = None
        self.rating = None
        self.sitter_id = None
        self.owner_id = None

        super(Stay, self).__init__(id)
