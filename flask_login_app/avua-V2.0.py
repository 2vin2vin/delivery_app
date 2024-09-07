# This code doesn't seem to work due to db issues
# Unable to create and use multiple instances of db at once


from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from distance import find_haversine
from osm_direction import generate_map

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['VENDOR_DATABASE_URI'] = 'sqlite://vendors.db'

app.config['ADMIN_DATABASE_URI'] = 'sqlite://admin.db'

app.config['DRIVER_DATABASE_URI'] = 'sqlite://driver.db'
duserb = SQLAlchemy(app)

class VendorDB:
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        self.db.engine = self.db.create_engine(app.config['VENDOR_DATABASE_URI'])

class AdminDB:
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        self.db.engine = self.db.create_engine(app.config['ADMIN_DATABASE_URI'])

class DriverDB:
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        self.db.engine = self.db.create_engine(app.config['DRIVER_DATABASE_URI'])

# Initialize custom SQLAlchemy instances for additional databases
vendordb = VendorDB(app)
admindb = AdminDB(app)
driverdb = DriverDB(app)

class User(userdb.Model):
    id = userdb.Column(userdb.Integer, primary_key=True)
    firstname = userdb.Column(userdb.String(150), nullable=False)
    lastname = userdb.Column(userdb.String(150), nullable=False)
    email = userdb.Column(userdb.String(150), unique=True, nullable=False)
    phonenumber = userdb.Column(userdb.String(20), nullable=False)
    username = userdb.Column(userdb.String(150), unique=True, nullable=False)
    password = userdb.Column(userdb.String(150), nullable=False)

# New Vendor model
class Vendor(vendordb.Model):
    id = vendordb.Column(vendordb.Integer, primary_key=True)
    vendorname = vendordb.Column(vendordb.String(150), nullable=False)
    vendorphone = vendordb.Column(vendordb.String(20), nullable=False)
    vendoremail = vendordb.Column(vendordb.String(150), nullable=False)
    vendorlat = vendordb.Column(vendordb.Float, nullable=False)
    vendorlon = vendordb.Column(vendordb.Float, nullable=False)
    vendorcity = vendordb.Column(vendordb.String(100), nullable=False)
    vendorstate = vendordb.Column(vendordb.String(100), nullable=False)
    vendorcountry = vendordb.Column(vendordb.String(100), nullable=False)
    password = vendordb.Column(vendordb.String(100), nullable=False)

# New Vendor listed items
class Vendor_listed_item(vendordb.Model):
    id = vendordb.Column(vendordb.Integer, primary_key=True)
    name = vendordb.Column(vendordb.String(100), nullable=False)
    category = vendordb.Column(vendordb.String(100), nullable=False)
    subcategory = vendordb.Column(vendordb.String(100), nullable=False)
    item_name = vendordb.Column(vendordb.String(100), nullable=False)
    price = vendordb.Column(vendordb.Float, nullable=False)
    quantity = vendordb.Column(vendordb.Integer, nullable=False)

# # New Category model
# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     parent_category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
#     children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))

@app.route('/admin_login', methods=['GET', 'POST'])
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
# 
# @app.route('/dashboard')
# def dashboard():
#     print("entered")
#     user_id = session.get('user_id')
#     if user_id:
#         user = db.session.get(User, user_id)  # Use Session.get() here
#         if request.method == "POST":
#             try:
#                 lat1=float(request.form.get('latitude'))
#                 lon1=float(request.form.get('longitude'))

#                 fl1,fl2 = find_haversine(lat1, lon1)
#                 return render_template('dashboard.html', user=user)

#                 #add more code to calculate distance and dispaly map
#             except ValueError:
#                 return render_template('dashboard.html', user=user, error_message='Enter valid inputs')
# #        if user:
#  #           return render_template('dashboard.html', user=user)
            
#     return redirect(url_for('login'))
            
# 
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
        if len(phonenumber)!=9:
            return render_template('register.html', error_message="Check Phone Number")
        
        if password != confirmpassword:
            return render_template('register.html', error_message="Passwords do not match!")
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(firstname=firstname,
                        lastname=lastname,
                        email=email,
                        phonenumber=phonenumber,
                        username=username,
                        password=hashed_password)
        
        try:
            userdb.session.add(new_user)
            userdb.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            userdb.session.rollback()
            return f'Error: {str(e)}'

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/vendor_login', methods=['GET', 'POST'])
def vendor_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        vendor = Vendor.query.filter_by(vendoremail=email).first()

        if vendor and check_password_hash(vendor.password, password):
            session['vendor_id'] = vendor.id
            return redirect(url_for('vendor_dashboard'))

        return render_template('vendor_login.html', error_message='Invalid credentials!')

    return render_template('vendor_login.html')

@app.route('/vendor_dashboard')
def vendor_dashboard():
    if 'vendor_id' in session:
        return render_template('vendor_dashboard.html')
        vendor = db.session.get(Vendor,session.get('vendor_id'))
        return f'Welcome, {vendor.vendorname}! This is your dashboard.'
    return redirect(url_for('vendor_login'))

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

        new_vendor = Vendor(vendorname=vendorname,
                            vendorphone=vendorphone,
                            vendoremail=vendoremail,
                            password=hashed_password,
                            vendorlat=vendorlat,
                            vendorlon=vendorlon,
                            vendorcity=vendorcity,
                            vendorstate=vendorstate,
                            vendorcountry=vendorcountry)
        
        try:
            vendordb.session.add(new_vendor)
            vendordb.session.commit()
            return redirect(url_for('vendor_login'))
        except Exception as e:
            vendordb.session.rollback()
            return f'Error: {str(e)}'

    return render_template('vendor_register.html')

@app.route('/vendor_logout')
def vendor_logout():
    session.pop('vendor_id', None)
    return redirect(url_for('vendor_login'))


if __name__ == '__main__':
    with app.app_context():
        userdb.create_all()  # Create database tables
        vendordb.create_all()
        admindb.create_all()
    app.run(debug=True)
