from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'id': self.id, 'email': self.email}

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Waiting", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    consultations = db.relationship('Consultation', backref='client', lazy=True, cascade="all, delete-orphan")
    enrollments = db.relationship('Enrollment', backref='client', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        enrollments = Enrollment.query.filter_by(client_id=self.id).all()
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'consultations': [c.id for c in self.consultations],
            'enrollments': [e.id for e in self.enrollments],
            'enrollments_data': [e.to_dict() for e in enrollments]
        }

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='programs')
    enrollments = db.relationship('Enrollment', backref='program', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'created_by': self.user.email,
            'updated_at': self.updated_at.isoformat(),
            'enrollments': [e.id for e in self.enrollments]
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'program_id': self.program_id,
            'created_at': self.created_at.isoformat()
        }

class Consultation(db.Model):
    __tablename__ = 'consultations'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    vitals = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    symptoms = db.Column(db.Text, nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    investigations = db.Column(db.Text, nullable=True)
    treatment_plan = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'vitals': self.vitals,
            'allergies': self.allergies,
            'symptoms': self.symptoms,
            'medical_history': self.medical_history,
            'medications': self.medications,
            'diagnosis': self.diagnosis,
            'investigations': self.investigations,
            'treatment_plan': self.treatment_plan,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }