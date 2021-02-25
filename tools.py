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


def help_msg():
    r = [
        "In order to add magic links type:",
        f"<code> /add [here goes magic link]</code>",
        f"The real magic starts with spell:",
        f"<code> /show [number of links, default 5]</code>",
        f"Please let us know you liked the link:",
        f"<code> /done [ID, ID2, etc]</code>",
        f"Other spells:",
        f"<code> /delete [ID]</code>",
        ]
    return r


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

