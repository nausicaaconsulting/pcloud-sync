import logging
import os
import sys

from flask import Flask

from sync.scheduler import start_scheduler
from sync.server.extensions import db, migrate

from sync.server.api import api_blueprint
from sync.server.admin import register_admin


def create_app(config_object="sync.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_admin(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    ###
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler()

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    return


def register_blueprints(app):
    app.register_blueprint(api_blueprint)
    return


def register_errorhandlers(app):
    pass


def register_shellcontext(app):
    def shell_context():
        return {"db": db}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    pass


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(name)s %(asctime)s]%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    # Clear default handler
    app.logger.handlers.clear()
    app.logger.addHandler(handler)

    # The werkzeug logger logs every call made to the flask app,
    # but sometimes it can be too verbose, as some call are made often and there is no
    # value in logging them
    # We add a filter to filter out the calls made by each process to update its status
    # see https://docs.python.org/3.9/library/logging.html#filter-objects
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addFilter(lambda record: '/api/1/process-info/update' not in record.getMessage())


#if __name__ == '__main__':
#    app = create_app()
#    app.run(debug=True)


