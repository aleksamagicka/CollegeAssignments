import json
import re

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt, \
    get_jwt_identity
from sqlalchemy import and_

from configuration import Configuration
from models import database, User

application = Flask(__name__)
application.config.from_object(Configuration)


@application.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    isCustomer = request.json.get("isCustomer", None)

    if (len(forename) == 0):
        return Response(json.dumps({"message": "Field forename is missing."}), status=400)
    if (len(surname) == 0):
        return Response(json.dumps({"message": "Field surname is missing."}), status=400)
    if (len(email) == 0):
        return Response(json.dumps({"message": "Field email is missing."}), status=400)
    if (len(password) == 0):
        return Response(json.dumps({"message": "Field password is missing."}), status=400)
    if isCustomer is None:
        return Response(json.dumps({"message": "Field isCustomer is missing."}), status=400)

    email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$)")
    if not re.fullmatch(email_regex, email):
        return Response(json.dumps({"message": "Invalid email."}), status=400)

    # Invalid password
    if not (any(char.isdigit() for char in password) and any(char.isupper() for char in password) and any(
            char.islower() for char in password)):
        return Response(json.dumps({"message": "Invalid password."}), status=400)

    if User.query.filter(User.email == email).count() > 0:
        return Response(json.dumps({"message": "Email already exists."}), status=400)

    user = User(email=email, password=password, forename=forename, surname=surname,
                role="customer" if isCustomer else "manager")
    database.session.add(user)
    database.session.commit()

    return Response(json.dumps({"message": "Registration successful!"}), status=200)


jwt = JWTManager(application)


@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0

    if emailEmpty:
        return Response(json.dumps({"message": "Field email is missing."}), status=400)
    if passwordEmpty:
        return Response(json.dumps({"message": "Field password is missing."}), status=400)

    email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$)")
    if not re.fullmatch(email_regex, email):
        return Response(json.dumps({"message": "Invalid email."}), status=400)

    user = User.query.filter(and_(User.email == email, User.password == password)).first()

    if (not user):
        return Response(json.dumps({"message": "Invalid credentials."}), status=400)

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "roles": user.role
    }

    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims)

    return jsonify(accessToken=accessToken, refreshToken=refreshToken)


@application.route("/check", methods=["POST"])
@jwt_required()
def check():
    return "Token is valid!"


@application.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    refreshClaims = get_jwt()

    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "roles": refreshClaims["roles"]
    }

    # return Response(json.dumps({"message": create_access_token(identity=identity, additional_claims=additionalClaims)}),
    #                status=200)

    return jsonify(accessToken=create_access_token(identity=identity, additional_claims=additionalClaims)), 200


@application.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    identity = get_jwt_identity()
    refreshClaims = get_jwt()
    if not "admin" in refreshClaims["roles"]:
        return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

    email = request.json.get("email", "")

    if len(email) == 0:
        return Response(json.dumps({"message": "Field email is missing."}), status=400)

    email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$)")
    if not re.fullmatch(email_regex, email):
        return Response(json.dumps({"message": "Invalid email."}), status=400)

    user = User.query.filter(User.email == email).first()
    if not user:
        return Response(json.dumps({"message": "Unknown user."}), status=400)

    database.session.delete(user)
    database.session.commit()

    return Response(status=200)


@application.route("/", methods=["GET"])
def index():
    return "Zdravo svete!"


if (__name__ == "__main__"):
    database.init_app(application);
    application.run(debug=True, host="0.0.0.0", port=5002)
