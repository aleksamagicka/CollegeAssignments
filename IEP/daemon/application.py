import collections
import json

from flask import Flask
from redis.client import Redis

from configuration import Configuration
from models import database, Category, Product, Order

application = Flask(__name__)
application.config.from_object(Configuration)


@application.route("/", methods=["GET"])
def index():
    return "Zdravo svete! Daemon"


if (__name__ == "__main__"):
    database.init_app(application)

    with Redis(Configuration.REDIS_URL) as redis:
        while True:
            new_array = json.loads(redis.blpop(Configuration.REDIS_LIST)[1].decode())
            print(f"ovo je json: {new_array}", flush=True)

            with application.app_context() as context:
                for split_product in new_array:
                    categories = split_product[0].split('|')
                    name = split_product[1]
                    quantity = int(split_product[2])
                    price = float(split_product[3])

                    # Proizvod sa istim imenom?
                    existing_product = Product.query.filter(Product.name == name).first()

                    if existing_product is None:
                        # Nema nijednog sa istim imenom

                        # Ubacivanje i provera kategorija
                        categories_list = list()
                        for category in categories:
                            category_query = Category.query.filter(Category.name == category).first()
                            if category_query is None:
                                category_query = Category(name=category)
                                database.session.add(category_query)
                            categories_list.append(category_query)

                        new_product = Product(name=name, quantity=quantity, price=price, categories=categories_list)
                        database.session.add(new_product)
                    else:
                        # Proizvod vec postoji

                        # Da li su kategorije ovog i postojeceg iste?
                        category_names = [c.name for c in existing_product.categories]
                        if collections.Counter(category_names) == collections.Counter(categories):
                            # Kategorije su iste, treba azurirati cenu proizvoda
                            current_quantity = existing_product.quantity
                            current_price = existing_product.price

                            delivered_quantity = quantity
                            delivered_price = price

                            new_price = (current_quantity * current_price + delivered_quantity * delivered_price) / (
                                    current_quantity + delivered_quantity)

                            existing_product.price = new_price
                            existing_product.quantity += quantity

                            # Provera da li nekim narudzbinama nedostaje trenutni proizvod
                            for order_request in sorted(existing_product.order_requests, key=lambda x: x.order.timestamp):
                                needs = order_request.requested - order_request.received
                                min_quantity = min(existing_product.quantity, needs)

                                order_request.received += min_quantity
                                existing_product.quantity -= min_quantity

                database.session.commit()
