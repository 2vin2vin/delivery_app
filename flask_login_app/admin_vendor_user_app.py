from flask import Flask, render_template, jsonify, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from distance import find_haversine
from osm_direction import generate_map
from sqlalchemy import DateTime
from db_miscalleneous import *
from flask_wtf.csrf import CSRFProtect


# Create database
# 1. Users
#   All User basic info
# Id      First Name    Last Name      Email                             Phone         Username         Password
# UR1024  Niranjan      Vishnubhatla   niranjan.vishnubhatla@gmail.com   9876543210    vnda vision      vnda vision
#   All their orders
# Id     Order Number       Item              Qunatity   price      Delivered time
# UR1024 OR3241         Iphone 15             1          150000     date and time
# 2. Vendors
#   All their info
# Id      Name              Phone       Email                      latitude  longitude   City        State     Country     Password
# VR1024  Rahul Donthula    9876543210  rahul.donthula@gmail.com   72.9876   17.7653     Hyderabad   Telangana India       rahul donthula
#   All their item list
# Id     Item Number  Item         Quantity  Price
# VR1024 IN1024       Iphone 15    10        150000  
# 3. Admin  
#   The order list that are pending
# Order Id      Driver     Delivery Time
# UR1024OR3241  DV1059     date and time
# 4. Driver
#   The driver info
# Id        Name           License         PAN         Aadhar         Home        Phone
# DV1059   Sohith          LC1234          PFDGH1234Q  1234567890    alwal        9876543210
#   The driver availability
# Id     Location           Free after time
# DV1059 alwal              date time model


app = Flask(__name__)
#3045ad9f2da9ccb8400963f98fbad27ccae5d2966729b20aa1c9e9e36e668824
app.config['SECRET_KEY'] = '3045ad9f2da9ccb8400963f98fbad27ccae5d2966729b20aa1c9e9e36e668824'  # Change this to a real secret key
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# 3. Admin  
#   The order list that are pending
# Order Id      Driver     Delivery Time
# UR1024OR3241  DV1059     date and time
class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = db.Column(db.String(50), primary_key=True)  # Assuming IDs like UR1024OR3241 are strings
    driver_id = db.Column(db.String(50), db.ForeignKey('drivers.d_id'), nullable=False)
    delivery_time = db.Column(DateTime, nullable=False)
    
    # Relationship with Driver
    driver = db.relationship('Driver', backref='orders', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.order_id} - Driver {self.driver_id}>'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        if email == 'admin':
            if password == 'nimad567':
                return redirect(url_for('dashboard'))

        return render_template('admin_login.html', error_message='Invalid credentials!')

    return render_template('admin_login.html')

@app.route('/')
def home():
    return render_template('login.html')


# Create database
# 1. Users
#   All User basic info
# Id      First Name    Last Name      Email                             Phone         Username         Password
# UR1024  Niranjan      Vishnubhatla   niranjan.vishnubhatla@gmail.com   9876543210    vnda vision      vnda vision

#   All their orders
# Id     Order Number       Item              Qunatity   price      Delivered time
# UR1024 OR3241         Iphone 15             1          150000     date and time
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(20), primary_key=True)  # User ID with prefix
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    orders = db.relationship('UserOrder', back_populates='user', lazy=True)

class UserOrder(db.Model):
    __tablename__ = 'user_order'
    uo_id = db.Column(db.String(20), primary_key=True)  # Primary key for UserOrder
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    ordernumber = db.Column(db.String(10), nullable=False)
    item = db.Column(db.String(250), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    deliveredtime = db.Column(DateTime, nullable=True)

    user = db.relationship('User', back_populates='orders')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('emailid')
        phonenumber = request.form.get('phonenumber')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        if not all([firstname, lastname, email, phonenumber, username, password, confirmpassword]):
            return render_template('register.html', error_message='All fields are required!')
        
        # the email is not getting recognised
        #check this as this did not show error condition
        if email.count('@')<0 or email.count('.')<0:
            return render_template('register.html', error_message='Check Email Id')
        
        #change the phone number to work with 10
        if len(phonenumber)!=10:
            return render_template('register.html', error_message="Check Phone Number")
        
        if password != confirmpassword:
            return render_template('register.html', error_message="Passwords do not match!")
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        idnumber = get_length_table('user')

        new_user = User(id='UR'+f"{idnumber:05}",
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        phonenumber=phonenumber,
                        username=username,
                        password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return f'Error: {str(e)}'

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        return render_template('login.html', error_message='Invalid credentials!')

    return render_template('login.html')
'''
@app.route('/dashboard')
def dashboard():
    print("entered")
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)  # Use Session.get() here
        if request.method == "POST":
            try:
                lat1=float(request.form.get('latitude'))
                lon1=float(request.form.get('longitude'))

                fl1,fl2 = find_haversine(lat1, lon1)
                return render_template('dashboard.html', user=user)

                #add more code to calculate distance and dispaly map
            except ValueError:
                return render_template('dashboard.html', user=user, error_message='Enter valid inputs')
#        if user:
 #           return render_template('dashboard.html', user=user)
            
    return redirect(url_for('login'))
            
'''

#change this as well to select and search
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        if request.method == 'POST':
            try:
                # Extract latitude and longitude from form
                lat1 = float(request.form.get('latitude'))
                lon1 = float(request.form.get('longitude'))

                fla, flo, dis = find_haversine(lat1, lon1)

                # Example predefined coordinates
#                predefined_points = [(12.9715987, 77.5945627), (13.0826802, 80.2707184)]

                # Calculate distances
#                distances = [calculate_distance(lat1, lon1, lat2, lon2) for lat2, lon2 in predefined_points]
#                closest_distance = min(distances) if distances else None
                print(str(lon1)+','+str(lat1),str(flo)+','+str(fla))
                generate_map(str(lon1)+','+str(lat1),str(flo)+','+str(fla))

                return render_template('dashboard.html', user=user, distance_result=dis/10, lat_result = fla, lon_result = flo)

            except ValueError:
                return render_template('dashboard.html', user=user, error_message='Invalid input. Please enter valid numbers.')

        return render_template('dashboard.html', user=user)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


# Add a function to
# 2. Vendors
#   All their info
# Id      Name              Phone       Email                      latitude  longitude   City        State     Country     Password
# VR1024  Rahul Donthula    9876543210  rahul.donthula@gmail.com   72.9876   17.7653     Hyderabad   Telangana India       rahul donthula

#   All their item list
# Id     Item Number  Category        Sub-Category       Item         Quantity  Price
# VR1024 IN1024       Electronics     Phones             Iphone 15    10        150000  
#  New Vendor model
class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    v_id = db.Column(db.String(20), primary_key=True)
    vendorname = db.Column(db.String(150), nullable=False)
    vendorphone = db.Column(db.String(20), nullable=False)
    vendoremail = db.Column(db.String(150), nullable=False)
    vendorlat = db.Column(db.Float, nullable=False)
    vendorlon = db.Column(db.Float, nullable=False)
    vendorcity = db.Column(db.String(100), nullable=False)
    vendorstate = db.Column(db.String(100), nullable=False)
    vendorcountry = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationship with Item
    items = db.relationship('VendorItem', backref='vendor', lazy=True)
    
    def __repr__(self):
        return f'<Vendor {self.vendorname}>'

class VendorItem(db.Model):
    __tablename__ = 'items'
    
    vi_id = db.Column(db.String(20), primary_key=True)
    vendor_id = db.Column(db.String(20), db.ForeignKey('vendors.v_id'), nullable=False)
    item_number = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    sub_category = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    
    def __repr__(self):
        return f'<Item {self.item}>'

@app.route('/vendor_register', methods=['GET', 'POST'])
def vendor_register():
    if request.method == 'POST':
        vendorname = request.form.get('vendorname')
        vendorphone = request.form.get('vendorphone')
        vendoremail = request.form.get('vendoremail')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        vendorlat = request.form.get('vendorlat')
        vendorlon = request.form.get('vendorlon')
        vendorcity = request.form.get('vendorcity')
        vendorstate = request.form.get('vendorstate')
        vendorcountry = request.form.get('vendorcountry')

        if not all([vendorname, vendorphone, vendoremail, password, confirmpassword, vendorlat, vendorlon, vendorcity, vendorstate, vendorcountry]):
            return render_template('vendor_register.html', error_message='All fields are required!')

        if password != confirmpassword:
            return render_template('vendor_register.html', error_message="Passwords do not match!")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        idnumber = get_length_table('user')

        new_vendor = Vendor(v_id="VR"+f"{idnumber:05}",
                            vendorname=vendorname,
                            vendorphone=vendorphone,
                            vendoremail=vendoremail,
                            password=hashed_password,
                            vendorlat=vendorlat,
                            vendorlon=vendorlon,
                            vendorcity=vendorcity,
                            vendorstate=vendorstate,
                            vendorcountry=vendorcountry)
        
        try:
            db.session.add(new_vendor)
            db.session.commit()
            return redirect(url_for('vendor_login'))
        except Exception as e:
            db.session.rollback()
            return f'Error: {str(e)}'

    return render_template('vendor_register.html')

@app.route('/vendor_login', methods=['GET', 'POST'])
@csrf.exempt
def vendor_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        vendor = Vendor.query.filter_by(vendoremail=email).first()

        if vendor and check_password_hash(vendor.password, password):
            session['vendor_id'] = vendor.v_id
            return redirect(url_for('vendor_dashboard'))

        return render_template('vendor_login.html', error_message='Invalid credentials!')

    return render_template('vendor_login.html')

#change this as the vendor dashboard should contain list of
#all the items in his db and add and delete options along with 
#edit
@app.route('/vendor_dashboard', methods=['GET','POST'])
def vendor_dashboard():
    print("Session:",dict(session))
    vendor_id = session.get('vendor_id')
    items_table=VendorItem.query.all()
    if vendor_id:
        vendor_details = db.session.get(Vendor, vendor_id)
        print("vendor details:", vendor_details)
        return render_template('vendor_dashboard.html', user=vendor_details, orders=items_table)
        
    return redirect(url_for('vendor_login'))

@app.route('/add_vendor_data', methods=['POST'])
@csrf.exempt
def add_vendor_data():
    # Get form data
    print("Entered add_output_data:",request.form)
    category = request.form.get('category')
    subcategory = request.form.get('subcategory')
    item_name = request.form.get('item_name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')

    # Retrieve the vendor_id and username from the session
    vendor_id = session.get('vendor_id')
    print(vendor_id,category,subcategory,item_name,price,quantity)
    last_id = get_id_from_table('items','vi_id')
    print("last_id:",last_id)
    if vendor_id:
        # Create a new Item record
        new_item = VendorItem(vendor_id=vendor_id,
            vi_id='IT'+f"{last_id:05}",
            category=category,
            item_number=0,
            sub_category=subcategory,
            item=item_name,
            price=price,
            quantity=quantity
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('vendor_dashboard'))  # Redirect to dashboard or any other page
    
    return redirect(url_for('vendor_login'))  # Redirect to login if vendor_id is not found

@app.route('/vendor_update_order', methods=['POST'])
def vendor_update_order():
    data = request.get_json()
    print("DATA:",data)
    order_id = data.get('id')
    new_price = data.get('price')
    new_quantity = data.get('quantity')
    item_del = VendorItem.query.get(order_id)
    if int(new_quantity)<1:
        db.session.delete(item_del)
        db.session.commit()

    order = VendorItem.query.get(order_id)
    if order:
        order.price = new_price
        order.quantity = new_quantity
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Order not found'}), 404

@app.route('/vendor_logout')
def vendor_logout():
    session.pop('vendor_id', None)
    return redirect(url_for('vendor_login'))

# 4. Driver
#   The driver info
# Id        Name           License         PAN         Aadhar         Home        Phone
# DV1059   Sohith          LC1234          PFDGH1234Q  1234567890    alwal        9876543210

#   The driver availability
# Id     Location           Free after time
# DV1059 alwal              date time model
class Driver(db.Model):
    __tablename__ = 'drivers'
    
    d_id = db.Column(db.String(20), primary_key=True)  # Assuming IDs like DV1059 are strings
    fullname = db.Column(db.String(150), nullable=False)
    drivinglicense = db.Column(db.String(50), nullable=False)
    pan = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    aadhar = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationship with DriverAvailability
    availability = db.relationship('DriverAvailability', backref='driver', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<Driver {self.fullname}>'

class DriverAvailability(db.Model):
    __tablename__ = 'driver_availabilities'
    
    da_id = db.Column(db.String(20), db.ForeignKey('drivers.d_id'), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    free_after = db.Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f'<DriverAvailability {self.id} - Free after {self.free_after}>'

@app.route('/driver_register', methods=['GET', 'POST'])
def driver_register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        drivinglicense = request.form.get('drivinglicense')
        pan = request.form.get('pan')
        email = request.form.get('email')
        aadhar = request.form.get('aadhar')
        phonenumber = request.form.get('phonenumber')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        print(fullname, drivinglicense, pan, email, aadhar, phonenumber, username, password, confirmpassword)

        if not all([fullname, drivinglicense, pan, email, aadhar, phonenumber, username, password, confirmpassword]):
            return render_template('driver_register.html', error_message='All fields are required!')
        
        # the email is not getting recognised
        #check this as this did not show error condition
        if email.count('@')<0 or email.count('.')<0:
            return render_template('driver_register.html', error_message='Check Email Id')
        
        #change the phone number to work with 10
        if len(phonenumber)!=10:
            return render_template('driver_register.html', error_message="Check Phone Number")
        
        if password != confirmpassword:
            return render_template('driver_register.html', error_message="Passwords do not match!")
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        idnumber = get_length_table('drivers')

        new_user = Driver(d_id='DR'+f"{idnumber:05}",
                        fullname=fullname,
                        drivinglicense=drivinglicense,
                        pan=pan,
                        aadhar=aadhar,
                        email=email,
                        phonenumber=phonenumber,
                        username=username,
                        password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('driver_login'))
        except Exception as e:
            db.session.rollback()
            return f'Error: {str(e)}'

    return render_template('driver_register.html')

@app.route('/driver_login', methods=['GET', 'POST'])
def driver_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Driver.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['d_id'] = user.d_id
            return redirect(url_for('driver_dashboard'))

        return render_template('driver_login.html', error_message='Invalid credentials!')

    return render_template('driver_login.html')

@app.route('/driver_dashboard', methods=['GET', 'POST'])
def driver_dashboard():
    print("Session:",dict(session))
    driver_id = session.get('d_id')
    print("s:",driver_id)
    if driver_id:
        driver_id = db.session.get(Driver, driver_id)
    print('g:',driver_id)
    return render_template('driver_dashboard.html',user=driver_id)

@app.route('/driver_logout')
def driver_logout():
    session.pop('d_id', None)
    return redirect(url_for('driver_login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
