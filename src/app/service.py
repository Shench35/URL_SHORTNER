import random
import string

characters = list(string.ascii_letters + string.digits)

def get_short_url():
    short = random.choices(characters,k=6)
    return ''.join(short)