from importlib import import_module
from pathlib import Path

import jinja_partials
from flask import Flask

from app.debug import show_headers
from app.extensions import htmx
from .db import init_db


def create_app():
    app = Flask(__name__)
    htmx.init_app(app)
    jinja_partials.register_extensions(app)
    register_blueprints(app)
    app.before_request(show_headers)
    return app


def register_blueprints(app):
    for path in Path(__file__).parent.glob("views/*.py"):
        module_name = path.stem
        if module_name.startswith("_"):
            continue
        module = import_module(f"app.views.{module_name}")
        blueprint = module.blueprint
        url_prefix = getattr(blueprint, "url_prefix", None)
        if url_prefix is None:
            url_prefix = f"/{module_name}"
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def main():
    app = create_app()
    init_db()
    app.run(debug=True)


if __name__ == "__main__":
    main()
