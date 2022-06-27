import csv
import io
import json

from flask import Flask, request, Response
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from redis.client import Redis

from configuration import Configuration
from models import database

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)


@application.route("/update", methods=["POST"])
@jwt_required()
def update():
    refreshClaims = get_jwt()
    if refreshClaims["roles"].strip() not in ["manager"]:
        return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

    if "file" not in request.files:
        return Response(json.dumps({"message": "Field file is missing."}), status=400)

    file = request.files['file'].stream.read()

    stream = io.StringIO(file.decode("UTF8"))
    reader = csv.reader(stream)

    products_list = list()

    for idx, line_parts in enumerate(reader):
        if len(line_parts) != 4:
            return Response(json.dumps({"message": f"Incorrect number of values on line {idx}."}), status=400)

        try:
            quantity = int(line_parts[2])
            if quantity < 0:
                raise ValueError()
        except ValueError:
            return Response(json.dumps({"message": f"Incorrect quantity on line {idx}."}), status=400)

        try:
            price = float(line_parts[3])
            if price < 0:
                raise ValueError()
        except ValueError:
            return Response(json.dumps({"message": f"Incorrect price on line {idx}."}), status=400)

        categories = line_parts[0].split('|')
        name = line_parts[1]

        # Salje se string dalje
        products_list.append(line_parts)

    with Redis(Configuration.REDIS_URL) as redis:
        redis.rpush(Configuration.REDIS_LIST, json.dumps(products_list))

    return Response(status=200)


@application.route("/", methods=["GET"])
def index():
    return "Zdravo svete! Warehouse"


if (__name__ == "__main__"):
    database.init_app(application);
    application.run(debug=True, host="0.0.0.0", port=5003)
