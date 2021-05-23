import os

from flask import Flask

import settings

from apps import db
from apps import views


def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder='../static', template_folder='../templates')
    app.config.from_object(settings)
    app.config.from_mapping(SECERT_KEY='dev', DATABASE=os.path.join(app.instance_path, 'apps.sqlite'))
    app.register_blueprint(views.bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    return app
