import datetime
import os
import pickle
import more_itertools


class Response:
    """
    Class for creating bot responses on telegram chat
    """
    def __init__(self, icon, title):
        self.title = f"<b>{icon} {title}</b>\n"
        self.separator = f"<b>---------------------------------------------</b>\n"
        self.lines = []
        self.body = [self.title, self.separator]
        self.add_lines()

    def add_lines(self):
        """
        Append lines list elements to body of object,
        each element is a new line in telegram chat
        """
        lines = more_itertools.collapse(self.lines)
        for line in lines:
            self.body.append(f"{line}\n")

    def print(self):
        """
        Return string made out of list elements (strings)
        """
        return ''.join(self.body)


class Link:
    """
    Class to store links and details
    """
    def __init__(self, time, url, author, votes, voters, msg_id):
        self.time = time
        self.url = url
        self.author = author
        self.votes = votes
        self.voters = voters
        self.msg_id = msg_id

    def __repr__(self):
        return f"{self.author}: {self.url}"


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
                        print('duplicat found: ', link)
                        return [True, link, i]
        return [False]

    def __repr__(self):
        return self.file


def time(pattern="%d/%m %H:%M"):
    """Return datetime object as string"""
    return datetime.datetime.now().strftime(pattern)


def icon_number(num):
    """Change integers or strings to icon numbers"""
    n = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣',
         '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    if num <= 10:
        return n[num]
    else:
        num = str(num)
        n_nums = []
        for x in range(len(num)):
            n_nums.append(n[int(num[x])])
        return "".join(n_nums)


def t_s(timestamp):
    """ Convert different timestamps to datetime object"""
    if len(str(timestamp)) == 13:
        time = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
    elif len(str(timestamp)) == 10:
        time = datetime.datetime.fromtimestamp(int(timestamp))
    elif len(str(timestamp)) == 16:
        time = datetime.datetime.fromtimestamp(int(timestamp / 1000000))
    elif len(str(timestamp)) == 12:
        time = datetime.datetime.fromtimestamp(int(timestamp.split('.')[0]))
    return time
