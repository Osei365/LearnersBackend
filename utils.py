import string
import random
from models.question import Question
from models import db

def generate_code(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))