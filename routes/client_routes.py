from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Client, Enrollment

# Resource for managing client data (CRUD operations)
class ClientResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
    parser.add_argument('age', type=int, required=True, help="Age cannot be blank")
    parser.add_argument('status', type=str, required=False)

# Handle GET request to fetch client(s); requires JWT authentication
    @jwt_required()
    def get(self, id=None):
        try:
            user_id = get_jwt_identity()
            search = request.args.get('search', '')
            status = request.args.get('status', '')
            print(f"Query params - search: {search}, status: {status}")  # Debug

            if id:
                client = Client.query.get_or_404(id)
                print(f"Fetching client with id {id}: {client.to_dict()}")  # Debug
                return client.to_dict(), 200

            query = Client.query
            if search:
                query = query.filter(Client.name.ilike(f'%{search}%'))
            if status:
                query = query.filter(Client.status.ilike(status))  
            clients = query.all()
            return [client.to_dict() for client in clients], 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

 # Handle POST request to create a new client; requires JWT authentication
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            args = self.parser.parse_args()
            client = Client(name=args['name'], age=args['age'], status="Waiting")
            db.session.add(client)
            db.session.commit()
            return client.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

# Handle PUT request to update an existing client; requires JWT authentication
    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            client = Client.query.get_or_404(id)
            args = self.parser.parse_args()
            client.name = args['name']
            client.age = args['age']
            client.status = args['status']
            db.session.commit()
            return client.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

 # Handle DELETE request to remove a client; requires JWT authentication
    @jwt_required()
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            client = Client.query.get_or_404(id)
            db.session.delete(client)
            db.session.commit()
            return {'message': 'Client deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500


# Resource for managing client enrollments in programs
class ClientEnrollmentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('programId', type=int, required=True, help="Program ID cannot be blank")

    @jwt_required()
    def post(self, client_id):
        try:
            user_id = get_jwt_identity()
            args = self.parser.parse_args()
            enrollment = Enrollment(client_id=client_id, program_id=args['programId'])
            db.session.add(enrollment)
            db.session.commit()
            return {'message': 'Client enrolled successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500