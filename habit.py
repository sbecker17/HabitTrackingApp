
from datetime import date


class Habit:

    def __init__(self, category, name, count, start_date):
        self.category = category
        self.name = name
        self.count = count
        self.start_date = start_date

    def __repr__(self):
        return "Habit('{}','{}','{}','{}',{})".format(self.category, self.name, self.count, self.start_date)
        