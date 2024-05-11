import string
import random

def generate_code(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def convert_date_to_string(dt):
    """converts datetime to string using 'month year' format"""
    return dt.strftime('%b %y')

