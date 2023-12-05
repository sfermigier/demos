from flask import Blueprint, render_template, request

from app.db import get_talks
from app.extensions import htmx

blueprint = Blueprint("search", __name__, url_prefix="/search")


@blueprint.get("/search")
def search():
    q = request.args.get("q", "").strip()
    talks = get_talks(q)

    if request.headers.get("HX-Trigger") == "search":
        return render_template("search/_rows.html", talks=talks)

    return render_template("search/index.html", talks=talks)


@blueprint.get("/search2")
def search2():
    q = request.args.get("q", "").strip()
    talks = get_talks(q)

    if htmx.trigger == "search":
        return render_template("search/_rows.html", talks=talks)

    return render_template("search/index.html", talks=talks)
