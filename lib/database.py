from playhouse.sqlite_ext import *

db = SqliteDatabase('db/transaction.db')


def create_tables():
    with db:
        db.create_tables([Transaction])


class Transaction(Model):
    id = CharField()
    data = JSONField()
    lunchmoney_id = SmallIntegerField(null=True)
    asset_id = SmallIntegerField()

    class Meta:
        database = db
