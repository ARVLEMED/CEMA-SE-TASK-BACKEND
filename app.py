from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from routes.auth_routes import LoginResource, SignupResource, UserResource
from routes.client_routes import ClientResource
from routes.program_routes import ProgramResource
from routes.consultation_routes import ConsultationResource
from routes.enrollment_routes import EnrollmentResource
from models import db, User, Client, Program, Enrollment, Consultation
import logging

app = Flask(__name__)
app.config.from_object(Config)

# CORS Configuration
CORS(app, resources={r"/api/*": {
    "origins": "http://localhost:5173",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

# Logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Register routes
api.add_resource(LoginResource, '/api/login')
api.add_resource(SignupResource, '/api/signup')
api.add_resource(UserResource, '/api/user')
api.add_resource(ClientResource, '/api/clients', '/api/clients/<int:id>')
api.add_resource(ProgramResource, '/api/programs', '/api/programs/<int:id>')
api.add_resource(ConsultationResource, '/api/consultations', '/api/consultations/<int:id>')
api.add_resource(EnrollmentResource, '/api/enrollments', '/api/enrollments/<int:id>')  # Updated to include 

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)