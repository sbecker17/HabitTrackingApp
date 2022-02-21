
class Habit:

    def __init__(self, category, name, count):
        self.category = category
        self.name = name
        self.count = count

    def __repr__(self):
        return "Habit('{}','{}',{})".format(self.category, self.name)
        