from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from distance import find_haversine
from osm_direction import generate_map

app = Flask(__name__)
#3045ad9f2da9ccb8400963f98fbad27ccae5d2966729b20aa1c9e9e36e668824
app.config['SECRET_KEY'] = '3045ad9f2da9ccb8400963f98fbad27ccae5d2966729b20aa1c9e9e36e668824'  # Change this to a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# New Vendor model
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendorname = db.Column(db.String(150), nullable=False)
    vendorphone = db.Column(db.String(20), nullable=False)
    vendoremail = db.Column(db.String(150), nullable=False)
    vendorlat = db.Column(db.Float, nullable=False)
    vendorlon = db.Column(db.Float, nullable=False)
    vendorcity = db.Column(db.String(100), nullable=False)
    vendorstate = db.Column(db.String(100), nullable=False)
    vendorcountry = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# New Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))


@app.route('/')
def home():
    return render_template('vendor_login.html')

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
                generate_map(str(lon1)+','+str(lat1),str(flo)+','+str(fla))

                return render_template('dashboard.html', user=user, distance_result=dis/10, lat_result = fla, lon_result = flo)

            except ValueError:
                return render_template('dashboard.html', user=user, error_message='Invalid input. Please enter valid numbers.')

        return render_template('dashboard.html', user=user)

    return redirect(url_for('login'))

@app.route('/vendor_dashboard')
def vendor_dashboard():
    if 'vendor_id' in session:
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
            db.session.add(new_vendor)
            db.session.commit()
            return redirect(url_for('vendor_login'))
        except Exception as e:
            db.session.rollback()
            return f'Error: {str(e)}'

    return render_template('vendor_register.html')

@app.route('/vendor_logout')
def vendor_logout():
    session.pop('vendor_id', None)
    return redirect(url_for('vendor_login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
