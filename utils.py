import string
import random
from pathlib import Path

from PIL import Image


def image_to_jpg(image_path):
    path = Path(image_path)
    if path.suffix not in {'.jpg', '.png', '.jfif', '.exif', '.gif', '.tiff', '.bmp'}:
        jpg_image_path = f'{path.parent / path.stem}_result.jpg'
        Image.open(image_path).convert('RGB').save(jpg_image_path)
        return jpg_image_path
    return image_path

def generate_code(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def convert_date_to_string(dt):
    """converts datetime to string using 'month year' format"""
    return dt.strftime('%b %y')

