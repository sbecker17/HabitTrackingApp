# for n in range(0, 7):
#     globals()['strg%s' % n] = 'Hello'
# strg0 = 'Hello', strg1 = 'Hello' ... strg6 = 'Hello'

for x in range(0, 7):
    globals()[f"variable1{x}"] = f"Hello the variable number {x}!"


print(variable15)


# other stuff I was messing around with:
#             globals()[f"h{x}"] = Habit( allHabits[x][0], allHabits[x][1], allHabits[x][2], allHabits[x][3], allHabits[x][4] )
#             item = globals()[x]
#             bob = f'h{x}'
#             print(type(f"h{x}"))
            