import json
from pathlib import Path

import dataset
from dataset import Table

db = dataset.connect("sqlite:///data/db.sqlite3")


def init_db():
    talks: Table = db["talks"]
    if talks.count() > 0:
        return

    for talk in json.load((Path("data") / "pyparis2018.json").open()):
        talks.insert(talk)


def get_talks(q: str) -> list[dict]:
    talks_table: Table = db["talks"]
    if not q:
        return talks_table.find(order_by=["title", "presenter"])

    table = talks_table.table
    statement = table.select(
        table.c.title.like(f"%{q}%") | table.c.presenter.like(f"%{q}%")
    )
    return db.query(statement, order_by=["title", "presenter"])
