from flask import Blueprint, render_template_string

# language=jinja2
# noinspection PyUnresolvedReferences
TEMPLATE = """
{% extends "_layout.html" %}
{% block content %}
<script src="https://unpkg.com/hyperscript.org@0.9.12"></script>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<button 
    hx-get="/confirmed"
    _="on htmx:confirm(issueRequest)
        halt the event
        call Swal.fire({
            title: 'Confirm', 
            text:'Do you want to continue?'
        })
        if result.isConfirmed issueRequest()
    ">
  Click Me
</button>
{% endblock %}
"""

blueprint = Blueprint("confirm", __name__)


@blueprint.route("/")
def index():
    return render_template_string(TEMPLATE)
