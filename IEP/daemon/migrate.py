import os
import shutil

from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database
from sqlalchemy_utils import database_exists, create_database, drop_database

dirpath = "/opt/src/daemon-migration/migrations"

if os.path.exists(dirpath) and os.path.isdir(dirpath):
    shutil.rmtree(dirpath)

application = Flask(__name__)
application.config.from_object(Configuration)

migrateObject = Migrate(application, database)

done = False
while not done:
    try:
        if (database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
            drop_database(application.config["SQLALCHEMY_DATABASE_URI"])

        create_database(application.config["SQLALCHEMY_DATABASE_URI"])

        database.init_app(application)

        with application.app_context() as context:
            database.create_all()
            init()
            migrate(message="Daemon migration")
            upgrade()

            database.session.commit()

            done = True
    except Exception as error:
        print(error)

while True:
    pass