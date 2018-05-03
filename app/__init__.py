from flask import Flask


def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)


def create_app(config=None):
    app = Flask(__name__)

    # load default configuration
    app.config.from_object('app.settings')

    register_web_blueprint(app)

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('./logs/app.log', maxBytes=1024 * 1024 * 10, backupCount=5)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    return app
