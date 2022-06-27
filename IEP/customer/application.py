import json

from flask import Flask, Response, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, get_jwt_identity

from configuration import Configuration
from models import database, Category, Product, Order, OrderRequest, User

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)


@application.route("/search", methods=["GET"])
@jwt_required()
def search():
    refreshClaims = get_jwt()
    if refreshClaims["roles"].strip() not in ["customer"]:
        return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

    product_name = request.args.get("name")
    category_name = request.args.get("category")

    categories_query = database.session.query(Category)
    products_query = database.session.query(Product)
    if category_name is not None:
        categories_query = categories_query.filter(Category.name.contains(category_name))

        products_query = products_query.filter(Product.categories.any(Category.name.contains(category_name)))

    if product_name is not None:
        categories_query = categories_query.filter(Category.products.any(Product.name.contains(product_name)))

        products_query = products_query.filter(Product.name.contains(product_name))

    categories = [c.name for c in categories_query.all()]
    products = [p.as_dict() | {"categories": [c.name for c in p.categories]} for p in products_query.all()]

    response = json.dumps({"categories": categories, "products": products})

    return Response(response, status=200)


@application.route("/order", methods=["POST"])
@jwt_required()
def order():
    refreshClaims = get_jwt()
    if refreshClaims["roles"].strip() not in ["customer"]:
        return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

    order_requests = request.json.get("requests", "")
    if len(order_requests) == 0:
        return Response(json.dumps({"message": "Field requests is missing."}), status=400)

    user_email = get_jwt_identity()

    order_requests_db = list()

    for idx, order_request in enumerate(order_requests):
        if 'id' not in order_request:
            return Response(json.dumps({"message": f"Product id is missing for request number {idx}."}), status=400)
        if 'quantity' not in order_request:
            return Response(json.dumps({"message": f"Product quantity is missing for request number {idx}."}),
                            status=400)

        try:
            int_id = int(order_request['id'])
            if int_id <= 0:
                raise ValueError
        except ValueError:
            return Response(json.dumps({"message": f"Invalid product id for request number {idx}."}), status=400)

        try:
            int_quantity = int(order_request['quantity'])
            if int_quantity <= 0:
                raise ValueError
        except ValueError:
            return Response(json.dumps({"message": f"Invalid product quantity for request number {idx}."}), status=400)

        product_from_db = Product.query.filter(Product.id == order_request['id']).first()
        if product_from_db is None:
            return Response(json.dumps({"message": f"Invalid product for request number {idx}."}), status=400)

        # Sad zapravo moze order
        order_request = OrderRequest(product=product_from_db, requested=int_quantity, received=0,
                                     product_price=product_from_db.price)

        # Prilikom kreiranja
        # narudžbine potrebno je ispuniti sve zahteve kupca ukoliko je to moguće. Za sve
        # neispunjene zahteve potrebno je sačekati novu dostavu proizvoda. Prilikom kreiranja
        # narudžbine za cenu proizvoda se uzima trenutna cena i nove dostave proizvoda neće
        # uticati na cenu narudžbine.

        min_quantity = min(product_from_db.quantity, order_request.requested)
        order_request.received += min_quantity
        product_from_db.quantity -= min_quantity

        order_requests_db.append(order_request)

    new_order = Order(requests=order_requests_db, user_email=user_email)
    database.session.add(new_order)
    database.session.commit()

    return Response(json.dumps({"id": new_order.id}), status=200)


@application.route("/status", methods=["GET"])
@jwt_required()
def status():
    refreshClaims = get_jwt()
    if refreshClaims["roles"].strip() not in ["customer"]:
        return Response(json.dumps({"msg": "Missing Authorization Header"}), status=401)

    user_orders = Order.query.filter(Order.user_email == get_jwt_identity()).all()
    orders_list = list()
    for idx, order in enumerate(user_orders):
        order_dict = {}
        order_sum = 0
        order_requested = 0
        order_received = 0

        order_products = list()

        for idx2, order_request in enumerate(order.requests):
            request_dict = {'categories': [c.name for c in order_request.product.categories],
                            'name': order_request.product.name, 'price': order_request.product_price,
                            'received': order_request.received, 'requested': order_request.requested}

            order_sum += order_request.product_price * order_request.requested
            order_received += order_request.received
            order_requested += order_request.requested

            order_products.append(request_dict)

        order_dict['products'] = order_products
        order_dict['price'] = order_sum
        order_dict['status'] = "COMPLETE" if order_requested == order_received else "PENDING"
        order_dict['timestamp'] = order.timestamp.isoformat()

        orders_list.append(order_dict)

    json_return = json.dumps({"orders": orders_list})
    print(f"status json: {json_return}", flush=True)

    return Response(json_return, status=200)


@application.route("/", methods=["GET"])
def index():
    return "Zdravo svete! Customer"


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5005)
