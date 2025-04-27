from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Program

class ProgramResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
    parser.add_argument('description', type=str)

    @jwt_required()
    def get(self, id=None):
        try:
            user_id = get_jwt_identity()
            search = reqparse.RequestParser().add_argument('search', type=str, location='args').parse_args()['search']
            if id:
                program = Program.query.get_or_404(id)
                return program.to_dict(), 200
            if search:
                programs = Program.query.filter(Program.name.ilike(f'%{search}%')).all()
            else:
                programs = Program.query.all()
            return [program.to_dict() for program in programs], 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            args = self.parser.parse_args()
            program = Program(user_id=int(user_id), name=args['name'], description=args['description'])
            db.session.add(program)
            db.session.commit()
            return program.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            program = Program.query.get_or_404(id)
            args = self.parser.parse_args()
            program.name = args['name']
            program.description = args['description']
            db.session.commit()
            return program.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            program = Program.query.get_or_404(id)
            db.session.delete(program)
            db.session.commit()
            return {'message': 'Program deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500