import random
import string
import time

from flask import Blueprint, render_template, request, render_template_string

blueprint = Blueprint("infinite_scroll", __name__)

# language=jinja2
INDEX_TEMPLATE = """
{% extends "_layout.html" %}
{% block content %}
<table hx-indicator="#ind">
  <thead>
  <tr>
    <th>Name</th>
    <th>Email</th>
    <th>ID</th>
  </tr>
  </thead>
  <tbody id="tbody">
  {% for contact in contacts %}
    {% if loop.last %}
      <tr hx-get="/infinite_scroll/contacts/?page=2" hx-trigger="revealed" hx-swap="afterend" hx-target="this">
        {% else %}
      <tr class="">
    {% endif %}
  <td>{{ contact.name }}</td>
  <td>{{ contact.email }}</td>
  <td>{{ contact.id }}</td>
  </tr>
  {% endfor %}
  </tbody>
</table>
<img id="ind" src="/static/img/bars.svg" class="htmx-indicator"/>
{% endblock %}
"""

# language=jinja2
PARTIAL_TEMPLATE = """
{% for contact in contacts %}
  {% if loop.last %}
    <tr hx-get="/infinite_scroll/contacts/?page={{ page + 1 }}" hx-trigger="revealed" hx-swap="afterend">
      {% else %}
    <tr class="">
  {% endif %}
    <td>{{ contact.name }}</td>
    <td>{{ contact.email }}</td>
    <td>{{ contact.id }}</td>
  </tr>
{% endfor %}
"""


@blueprint.route("/", defaults={"page": 1})
def index(page):
    contacts = generate_contacts(page=page)
    return render_template_string(INDEX_TEMPLATE, contacts=contacts, page=page)


@blueprint.route("/contacts/")
def contacts():
    page = int(request.args.get("page", 1))
    time.sleep(1)
    contacts = generate_contacts(page=page)
    return render_template_string(PARTIAL_TEMPLATE, contacts=contacts, page=page)


def generate_contacts(page=1, page_size=20):
    def generate_contact(i):
        def generate_id(n=15):
            return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))

        return {
            "name": "Agent Smith",
            "email": f"void{10 + (page - 1) * page_size + i}@null.org",
            "id": generate_id(),
        }

    return [generate_contact(i) for i in range(page_size)]
