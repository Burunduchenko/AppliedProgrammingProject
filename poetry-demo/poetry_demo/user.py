from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from models import User, Session
from validation_schemas import UserSchema

user = Blueprint('user', __name__)
bcrypt = Bcrypt()

session = Session()


# Get user by id
@user.route('/api/v1/user/<userId>', methods=['GET'])
def get_user(userId):
    # Check if user exists
    db_user = session.query(User).filter_by(id=userId).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')

    # Return user data
    user_data = {'id': db_user.id, 'name': db_user.name, 'surname': db_user.surname, 'username': db_user.username}
    return jsonify({"user": user_data})


# Update user by id
@user.route('/api/v1/user/<userId>', methods=['PUT'])
def update_user(userId):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user exists
    db_user = session.query(User).filter_by(id=userId).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')

    # Check if username is not taken if user tries to change it
    if db_user.username != data['username']:
        exists = session.query(User.id).filter_by(username=data['username']).first()
        if exists:
            return Response(status=400, response='User with such username already exists.')
    # Change user data
    db_user.name = data['name']
    db_user.surname = data['surname']
    hashed_password = bcrypt.generate_password_hash(data['password'])
    db_user.password = hashed_password
    db_user.username = data['username']

    # Save changes
    session.commit()

    # Return new user data
    user_data = {'id': db_user.id, 'name': db_user.name, 'surname': db_user.surname, 'username': db_user.username}
    return jsonify({"user": user_data})


# Delete user by id
@user.route('/api/v1/user/<userId>', methods=['DELETE'])
def delete_user(userId):
    # Check if user exists
    db_user = session.query(User).filter_by(id=userId).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')

    # Delete user
    session.delete(db_user)
    session.commit()
    return Response(response='User was deleted.')