"""
abstract base for class database table operations
"""
from abc import ABCMeta
import StringIO
from nover.data_access.database import Database


class Table(Database):
    """
    abstract base class for database table operations
    """

    __metaclass__ = ABCMeta

    def __init__(self, id=None):
        """
        constructor.
        derives database name from class name
        populates data from database

        args:
             id: None for new record, int for existing record
        """
        super(Table, self).__init__()
        self.id = id
        self._table = self._db[self.__class__.__name__.lower()]
        self.refresh(id)

    def __repr__(self):
        """
        representation of record for debugging

        args: --
        returns: string representation of object
        """
        output = StringIO.StringIO()
        output.write("\n")
        for column, value in sorted(self.__dict__.items()):
            output.write("{:<15} : {}\n".format(column, value))
        output.write("\n")
        return output.getvalue()

    def refresh(self, id=None):
        """
        populates object with data from database

        args:
             id: None for new record, int for existing
        returns:
             self
        """

        if hasattr(self, "id") and self.id is not None:
            id = self.id

        if id:
            result = self._table.find_one(id=id)
            if result is not None:
                # this is a bit tricky.  if the attribute begins with the
                # text "calculated_" that means that this attribute is a
                # descriptor ("calculated attribute"). we ensure that in
                # that instance we load the data from the appropriate
                # database column into the right attribute
                #
                # ex: database column: name  -> loads -> object.attribute: calculated_name
                self.__dict__.update({column: value for column, value in result.items()
                                      if "calculated_"+column not in self.__dict__})

                self.__dict__.update({"calculated_{}".format(column): value for
                                      column, value in result.items()
                                      if "calculated_"+column in self.__dict__})
        return self

    def save(self):
        """
        saves object attributes to database

        args: --
        returns: success
        """
        # if the attribute begins with the text "calculated_" that means
        # that this attribute is a descriptor ("calculated attribute"). we
        # ensure that in that instance we save the data from the attribute
        # into the appropriate database column
        #
        # ex: database column: name  -> loads -> object.attribute: calculated_name

        data = {column: value for column, value in self.__dict__.items()
                if not column.startswith("_") and not column.startswith("calculated_")}

        data.update({column[11:]: value for column, value in self.__dict__.items()
                     if column.startswith("calculated_")})

        try:
            result = self._table.upsert(data, ['id'])
            if not isinstance(result, bool):
                self.id = result
            self._db.commit()
        except Exception as error:
            print "error in save"
            self._db.rollback()
            raise error

    def delete(self):
        """
        delete the record from the database
        """

        try:
            if self.id is not None:
                self._table.delete(id=self.id)
                self._db.commit()
        except Exception as error:
            print "error in delete"
            raise error
