from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration (Render/Cloud Postgres yoo jiraate suni fayyadama, yoo dhabe local SQLite fayyadama)
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///hrkmso.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Member(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    promotionDate = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    hireYear = db.Column(db.String(20))
    birthYear = db.Column(db.String(20))
    rankSalary = db.Column(db.Float, default=0.0)
    locationAllowance = db.Column(db.Float, default=0.0)
    foodAllowance = db.Column(db.Float, default=0.0)
    eduLevel = db.Column(db.String(50))
    fieldOfStudy = db.Column(db.String(100))
    jobPosition = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Active')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    branch = db.Column(db.String(100))
    date = db.Column(db.String(20))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin_hrkmso').first():
        default_admin = User(username='admin_hrkmso', password='admin123', role='Admin', branch='', date='2026-01-01')
        db.session.add(default_admin)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/members', methods=['GET', 'POST'])
def handle_members():
    if request.method == 'POST':
        data = request.json
        new_member = Member(
            id=data.get('id'),
            name=data.get('name'),
            branch=data.get('branch'),
            rank=data.get('rank'),
            promotionDate=data.get('promotionDate'),
            gender=data.get('gender'),
            hireYear=data.get('hireYear'),
            birthYear=data.get('birthYear'),
            rankSalary=data.get('rankSalary', 0.0),
            locationAllowance=data.get('locationAllowance', 0.0),
            foodAllowance=data.get('foodAllowance', 0.0),
            eduLevel=data.get('eduLevel'),
            fieldOfStudy=data.get('fieldOfStudy'),
            jobPosition=data.get('jobPosition'),
            status=data.get('status', 'Active')
        )
        db.session.merge(new_member)
        db.session.commit()
        return jsonify({"message": "Success"}), 200

    members = Member.query.all()
    result = []
    for m in members:
        result.append({
            'id': m.id, 'name': m.name, 'branch': m.branch, 'rank': m.rank,
            'promotionDate': m.promotionDate, 'gender': m.gender, 'hireYear': m.hireYear,
            'birthYear': m.birthYear, 'rankSalary': m.rankSalary, 'locationAllowance': m.locationAllowance,
            'foodAllowance': m.foodAllowance, 'eduLevel': m.eduLevel, 'fieldOfStudy': m.fieldOfStudy,
            'jobPosition': m.jobPosition, 'status': m.status
        })
    return jsonify(result)

@app.route('/api/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        data = request.json
        new_user = User(
            username=data.get('username'),
            password=data.get('password'),
            role=data.get('role'),
            branch=data.get('branch', ''),
            date=data.get('date', '')
        )
        db.session.merge(new_user)
        db.session.commit()
        return jsonify({"message": "Success"}), 200

    users = User.query.all()
    result = []
    for u in users:
        result.append({
            'username': u.username, 'password': u.password,
            'role': u.role, 'branch': u.branch, 'date': u.date
        })
    return jsonify(result)

@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    if username == 'admin_hrkmso':
        return jsonify({"error": "Cannot delete main admin"}), 400
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)