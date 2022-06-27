import os
import shutil

from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database, User
from sqlalchemy_utils import database_exists, create_database, drop_database

dirpath = "/opt/src/authentication/migrations"

if os.path.exists(dirpath) and os.path.isdir(dirpath):
    shutil.rmtree(dirpath)

application = Flask(__name__)
application.config.from_object(Configuration)

migrateObject = Migrate(application, database)

done = False
while not done:
    try:
        if(database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
            drop_database(application.config["SQLALCHEMY_DATABASE_URI"])

        create_database(application.config["SQLALCHEMY_DATABASE_URI"])

        database.init_app(application)

        # Za daemon: Ali pazi da napraviš novi app context svaki put nakon što primiš poruku preko Redis jer inače se ne vide podaci koji su izmenjeni iz aplikacije za kupce

        with application.app_context() as context:
            init()
            migrate(message="Production migration")
            upgrade()

            admin = User(
                email="admin@admin.com",
                password="1",
                forename="admin",
                surname="admin",
                role="admin"
            )

            database.session.add(admin)
            database.session.commit()

            done = True
    except Exception as error:
        print(error)

while True:
    pass