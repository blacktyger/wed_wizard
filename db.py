import os
import pickle

from tools import Link, time, User


class Database:
    """
    Class to store data from bot app, links, users etc
    """
    def __init__(self, name):
        self.file = f'{name}.pickle'
        if not os.path.exists(self.file):
            self.table = {
                'info': {'created': time(pattern="%d/%m%y %H:%M:%S")},
                'links': [], 'users': {}, 'admins': []
                }
            self.save(self.table)

    def save(self, data):
        """
        Save to file pickle object of database
        """
        with open(self.file, 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def add_link(self, object):
        """
        Add Link object to database
        """
        db_snapshot = self.read()
        if isinstance(object, Link):
            link = self.get_link(object)
            if not link[0]:
                db_snapshot['links'].append(object)
                self.save(db_snapshot)
                return True
            else:
                return False
        else:
            return False

    def read(self):
        """
        Return pickled database as dict
        """
        with open(self.file, 'rb') as handle:
            return pickle.load(handle)

    def get_users(self):
        return self.read()['users']

    def get_user(self):
        """
        Look for User object in database that match input object,
        Return [bool, object, index]
        """

    def add_user(self, user):
        """
        Add User object to database
        """
        params = {
            'id': user.id,
            'is_bot': user.is_bot,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'language_code': user.language_code,
            }
        user = User(**params)
        db_snapshot = self.read()

        if user.id not in db_snapshot['users'].keys():
            db_snapshot['users'][user.id] = user
            self.save(db_snapshot)
            return [True, user]
        else:
            return [False, user.username]

    def get_links(self):
        return self.read()['links']

    def get_link(self, object):
        """
        Look for Link object in database that match input object,
        Return [bool, object, index]
        """
        db_snapshot = self.read()
        for i, link in enumerate(db_snapshot['links']):
            for k, v in vars(link).items():
                if k == 'url':
                    if v == object.url:
                        print('duplicate found: ', link)
                        return [True, link, i]
        return [False]

    def update_link(self, object):
        """
        Update Link object values if present in database
        """
        db_snapshot = self.read()
        link = self.get_link(object)
        if link[0]:
            db_snapshot['links'][link[2]] = object
            self.save(db_snapshot)

    def remove_link(self, object):
        """
        Remove Link object with given ID (list index)
        """
        db_snapshot = self.read()
        link = self.get_link(object)
        # print(link)
        if link[0]:
            db_snapshot['links'].remove(db_snapshot['links'][link[2]])
            self.save(db_snapshot)

    def remove_all_links(self):
        """
        Remove all Link objects from database
        """
        db_snapshot = self.read()
        db_snapshot['links'] = []
        self.save(db_snapshot)

    def __repr__(self):
        return self.file