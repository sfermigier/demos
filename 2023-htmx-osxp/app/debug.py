from devtools import debug
from flask import request


def show_headers():
    headers = request.headers
    hx_headers = {
        k: headers[k]
        for k in sorted(request.headers.keys())
        if k.lower().startswith("hx-")
    }
    debug(hx_headers)
