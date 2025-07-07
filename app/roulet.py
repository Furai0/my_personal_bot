

import random



def roulet():
    ints_for_random = range(0, 37)
    number = random.choice(ints_for_random)
    if number == 0:
        result =f'Выпало\n0\nЗеро 🟩\n😮'
    if number % 2 == 0 and number != 0:
        result = f'Выпало\n{number}\nЧерное ⬛️'
    if number % 2 != 0 and number != 0:
        result = f'Выпало\n{number}\nКрасное 🟥'
    return result