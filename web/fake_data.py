import string
import random

letters = string.ascii_letters + string.digits + '_'


def get_random_letters(count):
    return ''.join(random.choices(letters, k=count))


def get_random_number(count):
    return ''.join(random.choices(string.digits, k=count))
