# access_categories.py
from .categories import CATEGORY_DICT

def print_category(category_code):
    category_name = CATEGORY_DICT.get(category_code)
    if category_name:
        return category_name
    else:
        print(f"Category with code '{category_code}' not found.")
        return 'not found'