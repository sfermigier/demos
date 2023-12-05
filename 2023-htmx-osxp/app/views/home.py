from flask import Blueprint, render_template

blueprint = Blueprint("home", __name__, url_prefix="/")


@blueprint.get("/")
def index():
    return render_template("index.html")
