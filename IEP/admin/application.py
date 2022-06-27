import json

from flask import Flask, Response, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, get_jwt_identity

from configuration import Configuration
from models import database, Category, Product, Order, OrderRequest, User

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)


@application.route("/productStatistics", methods=["GET"])
@jwt_required()
def product_statistics():
    refreshClaims = get_jwt()
    if refreshClaims["roles"].strip() not in ["admin"]:
        return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

    statistics_list = list()
    products = Product.query.all()
    for product in products:
        product_dict = {'name': product.name}

        no_sold = 0
        no_waiting = 0

        for order_request in product.order_requests:
            no_sold += order_request.requested
            no_waiting += order_request.requested - order_request.received

        product_dict['sold'] = no_sold
        product_dict['waiting'] = no_waiting

        if no_sold > 0:
            statistics_list.append(product_dict)

    return Response(json.dumps({"statistics": statistics_list}), status=200)


@application.route("/categoryStatistics", methods=["GET"])
@jwt_required()
def category_statistics():
    refreshClaims = get_jwt()
    if refreshClaims["roles"].strip() not in ["admin"]:
        return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

    categories_counter = {}
    for c in Category.query.all():
        categories_counter[c.name] = 0

    for product in Product.query.all():
        for order_request in product.order_requests:
            for c in product.categories:
                categories_counter[c.name] += order_request.requested

    sorted_categories = sorted(categories_counter.items(), key=lambda x: (-x[1], x[0]))

    print(f"kategorije: {sorted_categories}, obicne: {categories_counter}", flush=True)

    sorted_category_names = [c[0] for c in sorted_categories]

    return Response(json.dumps({"statistics": sorted_category_names}), status=200)


@application.route("/", methods=["GET"])
def index():
    return "Zdravo svete! Admin"


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5006)
