# category_tree.py
class Category:
    def __init__(self, code, name, subcategories=None):
        self.code = code
        self.name = name
        self.subcategories = subcategories if subcategories is not None else {}

    def add_subcategory(self, code, name):
        self.subcategories[code] = Category(code, name)

    def get_subcategory(self, code):
        return self.subcategories.get(code)
    
    def print_hierarchy(self, level=0):
        indent = '  ' * level
        print(f"{indent}{self.code}: {self.name}")
        for subcategory in self.subcategories.values():
            subcategory.print_hierarchy(level + 1)

    def __repr__(self):
        return f"Category(code='{self.code}', name='{self.name}', subcategories={self.subcategories})"


class CategoryTree:
    def __init__(self):
        self.categories = {
            '1': Category('1', 'Electronics', {
                '1.1': Category('1.1', 'Phones & Accessories'),
                '1.2': Category('1.2', 'Laptops & Computers'),
                '1.3': Category('1.3', 'Tablets'),
                '1.4': Category('1.4', 'Cameras & Camcorders'),
                '1.5': Category('1.5', 'Audio & Headphones'),
                '1.6': Category('1.6', 'Wearable Technology'),
                '1.7': Category('1.7', 'Home Appliances')
            }),
            '2': Category('2', 'Clothing, Shoes & Accessories', {
                '2.1': Category('2.1', 'Men’s Clothing'),
                '2.2': Category('2.2', 'Women’s Clothing'),
                '2.3': Category('2.3', 'Kids’ Clothing'),
                '2.4': Category('2.4', 'Shoes'),
                '2.5': Category('2.5', 'Accessories', {
                    '2.5.1': Category('2.5.1', 'Jewelry'),
                    '2.5.2': Category('2.5.2', 'Belts'),
                    '2.5.3': Category('2.5.3', 'Hats')
                })
            }),
            '3': Category('3', 'Home, Furniture & Appliances', {
                '3.1': Category('3.1', 'Furniture', {
                    '3.1.1': Category('3.1.1', 'Living Room'),
                    '3.1.2': Category('3.1.2', 'Bedroom')
                }),
                '3.2': Category('3.2', 'Home Decor'),
                '3.3': Category('3.3', 'Kitchen & Dining'),
                '3.4': Category('3.4', 'Bedding & Mattresses'),
                '3.5': Category('3.5', 'Appliances')
            }),
            '4': Category('4', 'Health & Beauty', {
                '4.1': Category('4.1', 'Personal Care'),
                '4.2': Category('4.2', 'Health & Wellness'),
                '4.3': Category('4.3', 'Makeup'),
                '4.4': Category('4.4', 'Skincare'),
                '4.5': Category('4.5', 'Haircare')
            }),
            '5': Category('5', 'Toys, Games & Video Games', {
                '5.1': Category('5.1', 'Toys', {
                    '5.1.1': Category('5.1.1', 'Action Figures'),
                    '5.1.2': Category('5.1.2', 'Dolls')
                }),
                '5.2': Category('5.2', 'Games', {
                    '5.2.1': Category('5.2.1', 'Board Games'),
                    '5.2.2': Category('5.2.2', 'Puzzles')
                }),
                '5.3': Category('5.3', 'Video Games & Consoles')
            }),
            '6': Category('6', 'Groceries', {
                '6.1': Category('6.1', 'Fresh Food'),
                '6.2': Category('6.2', 'Pantry Staples'),
                '6.3': Category('6.3', 'Beverages'),
                '6.4': Category('6.4', 'Snacks'),
                '6.5': Category('6.5', 'Household Essentials')
            }),
            '7': Category('7', 'Sports & Outdoors', {
                '7.1': Category('7.1', 'Exercise & Fitness Equipment'),
                '7.2': Category('7.2', 'Outdoor Recreation'),
                '7.3': Category('7.3', 'Sports Apparel'),
                '7.4': Category('7.4', 'Camping & Hiking Gear')
            }),
            '8': Category('8', 'Automotive', {
                '8.1': Category('8.1', 'Car Electronics & GPS'),
                '8.2': Category('8.2', 'Car Care'),
                '8.3': Category('8.3', 'Tires & Wheels'),
                '8.4': Category('8.4', 'Tools & Equipment')
            })
        }

    def get_category(self, code):
        return self.categories.get(code)
    
    def print_tree(self):
        for category in self.categories.values():
            category.print_hierarchy()

    def __repr__(self):
        return f"CategoryTree(categories={self.categories})"
