from flask import Flask


def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)


def create_app(test_config=None):
    app = Flask(__name__)

    # load default configuration
    app.config.from_object('app.config')
    if test_config is not None:
        app.config.from_mapping(test_config)

    register_web_blueprint(app)

    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('./logs/app.log', maxBytes=1024 * 1024 * 10, backupCount=5)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    return app
