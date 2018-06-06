"""
object mapping to the sitter table
"""

from example.data_access.table import Table


class Sitter(Table):
    """
    object mapping to the sitter table
    """

    def __init__(self, id=None):
        """
        constructor

        args:
             id : None if new record / row id for record
        """
        self.id = id
        self.image = None
        # using the prefix calculated_ to signal to the attribute
        # conversion method that this is a decorated value
        # and to deal with the database column name conversion accordingly
        self.calculated_name = None
        self.phone = None
        self.email = None
        self.ratings_score = None
        self.score = None
        self.overall_rank = None
        super(Sitter, self).__init__(id)

    @property
    def name(self):
        """
        returns the value for name which is stored in the
        attribute calculated_name
        """
        return self.calculated_name

    @name.setter
    def name(self, val=None):
        """
        calculates the score based on the name before
        storing the name value in the calculated_name
        attribute

        args:
            val: the sitter name

        return:
            None
        """
        self.calculated_name = val
        self.score = (len(set(val.lower())) / (26 * 1.0)) * 5
