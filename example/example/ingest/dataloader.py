"""
data loader for csv file
"""

import os
import re

from collections import defaultdict
from example.data_access.database import Database
from example.tables.dog import Dog
from example.tables.owner import Owner
from example.tables.sitter import Sitter
from example.tables.stay import Stay


class DataLoader(object):
    """
    loads data from csv file into sqlite database
    """

    def __init__(self):
        """
        initialize and run the data load

        args: --
        """

        # only used during development
        # os.system("rm sqlite_db/example.sqlite")

        # remove database file before loading to start fresh
        if os.path.isfile("sqlite_db/example.sqlite"):
            print "remove database file before continuing!"
            exit()

        # load schema
        os.system("sqlite3 sqlite_db/example.sqlite < sqlite_db/schema.sql")

        # headers from the csv file
        csv_header = ["rating",
                      "sitter_image",
                      "end_date",
                      "text",
                      "owner_image",
                      "dogs",
                      "sitter",
                      "owner",
                      "start_date",
                      "sitter_phone_number",
                      "sitter_email",
                      "owner_phone_number",
                      "owner_email"]

        # take running total to do some tests of the load
        count_sitters = defaultdict(int)
        count_owners = defaultdict(int)
        count_stays = defaultdict(int)
        count_dogs = defaultdict(int)

        try:

            dog_by_owner_id = defaultdict(dict)

            with open("example/ingest/reviews.csv", "r") as fh:
                fh.readline()  # skip headers
                for line in fh:
                    if line.isspace():
                        continue
                    values = line.split(",")

                    # data contains the key,val pair of column name:value
                    data = dict(zip(csv_header, values))

                    sitter_id = self.populate_sitter(data)
                    count_sitters[sitter_id] += 1

                    owner_id = self.populate_owner(data)
                    count_owners[owner_id] += 1

                    stay_id = self.populate_stay(data, sitter_id, owner_id)
                    count_stays[stay_id] += 1

                    # is is possible for an owner to have many dogs and only a subset
                    # of those dogs show up for any given stay? yes? if so we need to
                    # account for that
                    for name in data['dogs'].split("|"):
                        name = name.strip()
                        dog_by_owner_id[owner_id][name] = True

            for owner_id in dog_by_owner_id:
                for dog_name in dog_by_owner_id[owner_id]:
                    dog_id = self.populate_dogs(dog_name, owner_id)
                    count_dogs[dog_id] += 1

        except Exception as error:
            print "could not ingest records from csv file"
            raise error

        db = Database()._db
        sitter_table = db['sitter']
        owner_table = db['owner']
        dog_table = db['dog']
        stay_table = db['stay']

        try:
            # check to ensure the record counts are correct
            assert sitter_table.count() == len(count_sitters.keys())
            assert owner_table.count() == len(count_owners.keys())
            assert dog_table.count() == len(count_dogs.keys())
            assert stay_table.count() == len(count_stays.keys())
        except Exception as error:
            print "ingestion record counts are not correct"
            raise error

    def id_from_image_path(self, string):
        """
        gets the id from the image path

        args:
            string: image path

        returns:
           id
        """
        match = re.match(r'.*user=(\d*)', string)
        return match.group(1)

    def populate_sitter(self, data):
        """
        inserts record into the sitter table

        args:
             data: dictionary representing row of csv

        returns:
            sitter record id
        """

        id = self.id_from_image_path(data['sitter_image'])
        sitter = Sitter(id)

        try:
            # tests if record already exists
            if sitter.image is not None:
                assert sitter.image == data['sitter_image']
            if sitter.name is not None:
                assert sitter.name == data['sitter']
            if sitter.phone is not None:
                assert sitter.phone == data['sitter_phone_number']
            if sitter.email is not None:
                assert sitter.email == data['sitter_email']
        except Exception as error:
            print "record already exists"
            raise error

        sitter.image = data['sitter_image']
        sitter.name = data['sitter']
        sitter.phone = data['sitter_phone_number']
        sitter.email = data['sitter_email']
        sitter.save()

        return sitter.id

    def populate_owner(self, data):
        """
        inserts record into the owner table

        args:
             data: dictionary representing row of csv

        returns:
            owner record id
        """

        id = self.id_from_image_path(data['owner_image'])
        owner = Owner(id)

        try:
            # confirms that record does not already exist
            if owner.image is not None:
                assert owner.image == data['owner_image']
            if owner.name is not None:
                assert owner.name == data['owner']
            if owner.phone_number is not None:
                assert owner.phone_number == data['owner_phone_number']
            if owner.email is not None:
                assert owner.email == data['owner_email']
        except Exception as error:
            print "record already exists"
            raise error

        owner.image = data['owner_image']
        owner.name = data['owner']
        owner.phone_number = data['owner_phone_number']
        owner.email = data['owner_email']
        owner.save()
        return owner.id

    def populate_stay(self, data, sitter_id, owner_id):
        """
        inserts record into the stay table

        args:
             data: dictionary representing row of csv
             sitter_id: foreign key sitter_id
             owner_id : foreign key owner_id

        returns:
            stay record id
        """
        stay = Stay()
        stay.review = data['text']
        stay.start_date = data['start_date']
        stay.end_date = data['end_date']
        stay.rating = data['rating']
        stay.sitter_id = sitter_id
        stay.owner_id = owner_id
        stay.save()
        return stay.id

    def populate_dogs(self, name, owner_id):
        """
        inserts record into the dogs table

        args:
             data: dictionary representing row of csv
             owner_id : foreign key owner_id

        returns:
            array of dog ids
        """
        name = name.strip()
        dog = Dog()
        dog.name = name
        dog.owner_id = owner_id
        dog.save()
        return dog.id


if __name__ == "__main__":
    pass
