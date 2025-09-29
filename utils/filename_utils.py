import os
import re

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_unique_filename(base_name, ext):
    filename = f"{base_name}.{ext}"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_name}({counter}).{ext}"
        counter += 1
    return filename
