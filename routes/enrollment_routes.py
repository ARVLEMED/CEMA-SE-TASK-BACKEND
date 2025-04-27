from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Enrollment, Client, Program

class EnrollmentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('client_id', type=int, required=True, help="Client ID cannot be blank")
    parser.add_argument('program_id', type=int, required=True, help="Program ID cannot be blank")

    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            enrollments = Enrollment.query.all()
            return [enrollment.to_dict() for enrollment in enrollments], 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            args = self.parser.parse_args()

            # Validate client and program existence
            client = Client.query.get_or_404(args['client_id'])
            program = Program.query.get_or_404(args['program_id'])

            # Check if the client is already enrolled in the program
            existing_enrollment = Enrollment.query.filter_by(
                client_id=args['client_id'],
                program_id=args['program_id']
            ).first()
            if existing_enrollment:
                return {'message': 'Client is already enrolled in this program'}, 400

            enrollment = Enrollment(
                client_id=args['client_id'],
                program_id=args['program_id']
            )
            db.session.add(enrollment)
            db.session.commit()
            return {'message': 'Client enrolled successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            enrollment = Enrollment.query.get_or_404(id)
            db.session.delete(enrollment)
            db.session.commit()
            return {'message': 'Client unenrolled successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500