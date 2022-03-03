
from datetime import date


class Habit:

    def __init__(self, username, category, name, count, start_date):
        self.username = username
        self.category = category
        self.name = name
        self.count = count
        self.start_date = start_date

    def __repr__(self):
        return "Habit('{}','{}','{}','{}','{}',{})".format(self.username, self.category, self.name, self.count, self.start_date)
        