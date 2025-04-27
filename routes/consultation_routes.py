from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Consultation, Client

# Resource for managing consultation data (CRUD operations)
class ConsultationResource(Resource):
    @jwt_required()
    def get(self, id=None):
        try:
            user_id = get_jwt_identity()
            if id:
                consultation = Consultation.query.get_or_404(id)
                return consultation.to_dict(), 200
            else:
                client_id = request.args.get('client_id', type=int)
                if client_id:
                    consultations = Consultation.query.filter_by(client_id=client_id).all()
                else:
                    consultations = Consultation.query.all()
                return [consultation.to_dict() for consultation in consultations], 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            parser = reqparse.RequestParser()
            parser.add_argument('client_id', type=int, required=True, help="Client ID cannot be blank")
            parser.add_argument('vitals', type=str)
            parser.add_argument('allergies', type=str)
            parser.add_argument('symptoms', type=str)
            parser.add_argument('medical_history', type=str)
            parser.add_argument('medications', type=str)
            parser.add_argument('diagnosis', type=str)
            parser.add_argument('investigations', type=str)
            parser.add_argument('treatment_plan', type=str)
            args = parser.parse_args()
            
            
            client = Client.query.get_or_404(args['client_id'])
            
            consultation = Consultation(
                client_id=args['client_id'],
                vitals=args.get('vitals'),
                allergies=args.get('allergies'),
                symptoms=args.get('symptoms'),
                medical_history=args.get('medical_history'),
                medications=args.get('medications'),
                diagnosis=args.get('diagnosis'),
                investigations=args.get('investigations'),
                treatment_plan=args.get('treatment_plan')
            )

            db.session.add(consultation)
            db.session.commit()
            return consultation.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            parser = reqparse.RequestParser()
            parser.add_argument('client_id', type=int, required=True, help="Client ID cannot be blank")
            parser.add_argument('vitals', type=str)
            parser.add_argument('allergies', type=str)
            parser.add_argument('symptoms', type=str)
            parser.add_argument('medical_history', type=str)
            parser.add_argument('medications', type=str)
            parser.add_argument('diagnosis', type=str)
            parser.add_argument('investigations', type=str)
            parser.add_argument('treatment_plan', type=str)
            args = parser.parse_args()


            consultation = Consultation.query.get_or_404(id)
            client = Client.query.get_or_404(args['client_id'])
            
            consultation.client_id = args['client_id']
            consultation.vitals = args.get('vitals')
            consultation.allergies = args.get('allergies')
            consultation.symptoms = args.get('symptoms')
            consultation.medical_history = args.get('medical_history')
            consultation.medications = args.get('medications')
            consultation.diagnosis = args.get('diagnosis')
            consultation.investigations = args.get('investigations')
            consultation.treatment_plan = args.get('treatment_plan')
            
            db.session.commit()
            return consultation.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

    @jwt_required()
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            consultation = Consultation.query.get_or_404(id)
            db.session.delete(consultation)
            db.session.commit()
            return {'message': 'Consultation deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500