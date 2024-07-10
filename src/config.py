import os

# Get the absolute path of the directory where the current file is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Define the database URI for SQLAlchemy, using SQLite database located in the same directory
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'weather_data.db')

# Disable modification tracking to save resources
SQLALCHEMY_TRACK_MODIFICATIONS = False
