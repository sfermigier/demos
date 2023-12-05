from devtools import debug
from lxml import etree, html

from flask import Blueprint, render_template, request

from app.db import get_talks
from app.debug import show_headers
from app.extensions import htmx

blueprint = Blueprint("search-alt", __name__, url_prefix="/search-alt")
parser = etree.HTMLParser()


@blueprint.get("/search")
def search():
    q = request.args.get("q", "").strip()
    talks = get_talks(q)
    return render_template("search/index.html", talks=talks)


@blueprint.after_request
def after_request(response):
    show_headers()

    if htmx.trigger:
        target = htmx.target
        debug(target)
        data = response.get_data()
        tree = html.fromstring(data, parser=parser)
        target_elem = tree.xpath(f"//*[@id='{target}']")[0]
        oob_elems = tree.xpath("//*[@hx-swap-oob]")
        elems = [target_elem] + oob_elems
        response.data = "".join([html.tostring(elem, encoding=str) for elem in elems])

    return response
