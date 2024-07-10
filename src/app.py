from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flasgger import Swagger
import os

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    # Create Flask app instance with static folder for Swagger UI
    app = Flask(__name__, static_folder='static')

    # Load configuration from config.py
    app.config.from_object('config')

    # Initialize SQLAlchemy with the app instance
    db.init_app(app)

    # Initialize Flask-RESTful API
    api = Api(app)

    # Import and add resource endpoints to the API
    from resources import WeatherResource, WeatherStatsResource
    api.add_resource(WeatherResource, '/api/weather')  # Endpoint for weather data
    api.add_resource(WeatherStatsResource, '/api/weather/stats')  # Endpoint for weather statistics

    # Initialize Swagger for API documentation
    swagger = Swagger(app)

    return app

if __name__ == '__main__':
    # Create the Flask application instance
    app = create_app()

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run the Flask development server
    app.run(debug=True)
