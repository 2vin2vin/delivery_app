# save_category_tree.py
import pickle
from category_tree.category_tree import CategoryTree

# Create an instance of CategoryTree
tree = CategoryTree()

# Save to a file
with open('./instance/category_tree.pkl', 'wb') as file:
    pickle.dump(tree, file)
