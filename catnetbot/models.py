import peewee

db = peewee.SqliteDatabase('catnet.db')


class Punishment(peewee.Model):
    punished_id = peewee.BigIntegerField()
    moderator_id = peewee.BigIntegerField()
    punishment_until = peewee.DateTimeField()
    punishment_reason = peewee.CharField(max_length = 200)

    class Meta:
        database = db