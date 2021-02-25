import os
import pickle

from tools import Link, time


class Database:
    """
    Class to store data from bot app, links, users etc
    """

    def __init__(self, name):
        self.file = f'{name}.pickle'
        if not os.path.exists(self.file):
            self.table = {
                'info': {'created': time(pattern="%d/%m%y %H:%M:%S")},
                'links': [], 'users': [], 'admins': []
                }
            self.save(self.table)

    def save(self, data):
        """
        Save to file pickle object of database
        """
        with open(self.file, 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def add(self, table, row):
        """
        Add Link object to database
        """
        db_snapshot = self.get()
        if isinstance(row, Link):
            link = self.find_row(row)
            if not link[0]:
                db_snapshot[table].append(row)
                self.save(db_snapshot)
                return True
            else:
                return False
        else:
            return False

    def update_link(self, row):
        """
        Update Link object values if present in database
        """
        db_snapshot = self.get()
        link = self.find_row(row)
        if link[0]:
            db_snapshot['links'][link[2]] = row
            self.save(db_snapshot)

    def remove_link(self, row):
        """
        Remove Link object with given ID (list index)
        """
        db_snapshot = self.get()
        link = self.find_row(row)
        # print(link)
        if link[0]:
            db_snapshot['links'].remove(db_snapshot['links'][link[2]])
            self.save(db_snapshot)

    def remove_all(self):
        """
        Remove all Link objects from database
        """
        db_snapshot = self.get()
        db_snapshot['links'] = []
        self.save(db_snapshot)

    def get_links(self):
        return self.get()['links']

    def get(self):
        """
        Return pickled database as dict
        """
        with open(self.file, 'rb') as handle:
            return pickle.load(handle)

    def find_row(self, row):
        """
        Look for object in database that match input object,
        Return [bool, object, index]
        """
        db_snapshot = self.get()
        for i, link in enumerate(db_snapshot['links']):
            for k, v in vars(link).items():
                if k == 'url':
                    if v == row.url:
                        print('duplicate found: ', link)
                        return [True, link, i]
        return [False]

    def __repr__(self):
        return self.file