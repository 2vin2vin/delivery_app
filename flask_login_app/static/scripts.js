// Categories and subcategories data
const data = {
    'Electronics': ['Phones & Accessories', 'Laptops & Computers', 'Tablets', 'Cameras & Camcorders', 'Audio & Headphones', 'Wearable Technology', 'Home Appliances'],
    'Clothes, Shoes & Accessories': ['Men’s Clothing', 'Women’s Clothing', 'Kids Clothing', 'Shoes', 'Accessories'],
    'Home, Furniture & Appliances': ['Furniture', 'Home Decor', 'Kitchen & Dining', 'Bedding & Mattresses', 'Appliances'],
    'Health & Beauty': ['Personal Care', 'Health & Wellness', 'Makeup', 'Skincare', 'Haircare'],
    'Toys, Games & Video Games': ['Toys', 'Games', 'Video Games & Consoles'],
    'Groceries': ['Fresh Food', 'Pantry Staples', 'Beverages', 'Snacks', 'Household Essentials'],
    'Sports & Outdoors': ['Exercise & Fitness Equipment', 'Outdoor Recreation', 'Sports Apparel', 'Camping & Hiking Gear'],
    'Automotive': ['Car Electronics & GPS', 'Car Care', 'Tires & Wheels', 'Tools & Equipment'],
    // Add more categories and subcategories here
};

// Populate categories dropdown
const categoryDropdown = document.getElementById('category');
for (const [key, value] of Object.entries(data)) {
    const option = document.createElement('option');
    option.value = key;
    option.textContent = `${key}`;
    categoryDropdown.appendChild(option);
}

// Populate subcategories based on selected category
function populateSubcategories() {
    const category = categoryDropdown.value;
    const subcategoryDropdown = document.getElementById('subcategory');
    const subcategoryContainer = document.getElementById('subcategory-container');
    const itemNameContainer = document.getElementById('item-name-container');
    const priceContainer = document.getElementById('price-container');
    const quantityContainer = document.getElementById('quantity-container');

    // Clear previous subcategories
    subcategoryDropdown.innerHTML = '<option value="">Select a subcategory</option>';

    if (category && data[category]) {
        data[category].forEach(sub => {
            const option = document.createElement('option');
            option.value = sub;
            option.textContent = sub;
            subcategoryDropdown.appendChild(option);
        });
        subcategoryContainer.style.display = 'block';
        itemNameContainer.style.display = 'block';
        priceContainer.style.display = 'block';
        quantityContainer.style.display = 'block';
    } else {
        subcategoryContainer.style.display = 'none';
        itemNameContainer.style.display = 'none';
        priceContainer.style.display = 'none';
        quantityContainer.style.display = 'none';
    }
}

// Handle form submission
document.getElementById('vendor-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    console.log('Form data submitted:', data);
    // You can process the form data here, e.g., send it to the server or display it
});
