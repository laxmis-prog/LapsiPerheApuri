import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context


# Import your app here to access its configuration
from flasky import create_app, db  # Replace with your actual import


def get_engine_url():
   return current_app.config["SQLALCHEMY_DATABASE_URI"]


config = context.config


# Interpret the config file for Python logging.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
   return current_app.extensions['migrate'].db.get_engine()


def get_engine_url():
   return current_app.config["SQLALCHEMY_DATABASE_URI"]


target_db = current_app.extensions['migrate'].db


def get_metadata():
   if hasattr(target_db, 'metadatas'):
       return target_db.metadatas[None]
   return target_db.metadata


def run_migrations_offline():
   url = get_engine_url()
   context.configure(
       url=url, target_metadata=get_metadata(), literal_binds=True
   )


   with context.begin_transaction():
       context.run_migrations()


def run_migrations_online():
   connectable = get_engine()


   with connectable.connect() as connection:
       context.configure(
           connection=connection,
           target_metadata=get_metadata(),
           include_schemas=True,  # Ensure schema support if needed
       )


       with context.begin_transaction():
           context.run_migrations()


if context.is_offline_mode():
   run_migrations_offline()
else:
   run_migrations_online()
