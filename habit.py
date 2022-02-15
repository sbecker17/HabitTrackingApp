
class Habit:

    def __init__(self, category, name):
        self.category = category
        self.name = name

    def __repr__(self):
        return "Habit('{}','{}',{})".format(self.category, self.name)
        