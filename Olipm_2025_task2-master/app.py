from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import Config
from models import db
from utils.errors import register_error_handlers
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Swagger(app)
    register_routes(app)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.logger.setLevel(logging.INFO)
    app.logger.info("Starting Education API...")
    app.run(host='0.0.0.0', port=5000)
