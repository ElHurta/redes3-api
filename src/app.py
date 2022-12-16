from flask import Flask
from routes.pop_routes import pop_routes
from routes.smtp_routes import smtp_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.register_blueprint(pop_routes)
    app.register_blueprint(smtp_routes)
    return app