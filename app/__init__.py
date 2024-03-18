from flask import Flask, render_template
from config import config
from .main import main
from flask_bootstrap import Bootstrap

def create_app(config_name):
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # attach routes and custom error pages here
    app.register_blueprint(main)
    return app