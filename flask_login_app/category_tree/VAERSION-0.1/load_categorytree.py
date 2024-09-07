# load_category_tree.py
import pickle
from category_tree.category_tree import CategoryTree

def load_tree(filepath='instance/category_tree.pkl'):
    with open(filepath, 'rb') as file:
        return pickle.load(file)

def get_list(tree, category_code='1'):
    category = tree.get_category(category_code)
    if category:
        category.print_hierarchy()
    else:
        print(f"Category with code '{category_code}' not found.")
    return category

if __name__ == "__main__":
    tree = load_tree()
    get_list(tree)  # Default to root category '1'
