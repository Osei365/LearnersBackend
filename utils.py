import string
import random
from models.question import Question
from models import db
from datetime import datetime

def generate_code(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def convert_date_to_string(dt, dt_format):
    """converts datetime to string using 'month year' format"""
    return datetime.strptime(dt, dt_format).strftime('%b %y')

