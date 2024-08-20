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
        
        #check this as this did not show error condition
        if email.count('@')<0 or email.count('.')<0:
            return render_template('register.html', error_message='Check Email Id')
        
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
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return f'Error: {str(e)}'

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
