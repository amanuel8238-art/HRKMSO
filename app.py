import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hrkmso_secret_key'

# Database Qindeessuu (Render irratti SQLite ykn PostgreSQL fayyadamuu dandeessa)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrkmso.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model / Gabatee Daataa (Personnel/Ogeessaaf)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False) # Fakkeenyaaf Dadar, kkf

    def __repr__(self):
        return f'<Employee {self.full_name}>'

# Database uumuu
with app.app_context():
    db.create_all()

# Fuula Duraa (Home)
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

# Ogeessa Dabaluu Route
@app.route('/add', methods=['POST'])
def add_employee():
    full_name = request.form.get('full_name')
    position = request.form.get('position')
    branch = request.form.get('branch')
    
    if full_name and position and branch:
        new_emp = Employee(full_name=full_name, position=position, branch=branch)
        db.session.add(new_emp)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)