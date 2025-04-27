from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

# Resource for handling user signup
class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        args = parser.parse_args()

        try:
            email = args['email']
            
            if User.query.filter_by(email=email).first():
                return {'message': 'Email already exists'}, 400
                
            user = User(email=email)
            user.set_password(args['password'])
            db.session.add(user)
            db.session.commit()
            
            access_token = create_access_token(identity=str(user.id))
            return {
                'message': 'User created successfully',
                'access_token': access_token,
                'user': user.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Server error: {str(e)}'}, 500

# Resource for handling user login
class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        args = parser.parse_args()

        try:
            user = User.query.filter_by(email=args['email']).first()
            if user and user.check_password(args['password']):
                access_token = create_access_token(identity=str(user.id))
                return {'access_token': access_token, 'user': user.to_dict()}, 200
            return {'message': 'Invalid credentials'}, 401
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

# Resource for retrieving authenticated user details
class UserResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get_or_404(user_id)
            return user.to_dict(), 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500
