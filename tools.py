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
        "<code>In order to add magic links type:</code>",
        f"/add [here goes magic link]",
        f"<code>The real magic starts with spell:</code>",
        f"/show",
        f"<code>Please like the magic links:</code>",
        f"/like LINK_ID",
        f"<code>Other spells:</code>",
        f"/delete LINK_ID",
        f"/show number (default is 5)",
        f"/like LINK_ID1 LINK_ID2 (You can chain IDs)",
        f"\n<a href='https://epicfundme.com/109'>Show some love @ EpicFundMe </a>",
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


class User:
    """
    Class manage User objects accounts
    """
    def __init__(self, id, username, is_bot, first_name):
        self.id = id
        self.first_name = first_name
        self.username = username
        self.is_bot = is_bot




