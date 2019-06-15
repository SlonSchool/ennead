from peewee import DatabaseProxy, Model


database = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database
