import os

from peewee import PostgresqlDatabase, Model
from peewee import TextField, CharField, FixedCharField, PrimaryKeyField, ForeignKeyField, DateTimeField, DateField, DecimalField, SmallIntegerField, BigIntegerField, BooleanField

db = PostgresqlDatabase(
    'eso',
    host=str(os.environ.get('HOST')),
    user=str(os.environ.get('USER')),
    password=str(os.environ.get('PASSWORD'))
)


class PeopleModel(Model):
    """A base model for the people schema for the inheritance usage"""

    class Meta:
        database = db
        schema = 'people'


class MembershipModel(Model):
    """A base model for the membership schema for the inheritance usage"""

    class Meta:
        database = db
        schema = 'membership'


class EventModel(Model):
    """A base model for the event schema for the inheritance usage"""

    class Meta:
        database = db
        schema = 'event'


class Person(PeopleModel):
    """Person table representation object"""
    id = PrimaryKeyField()
    first_name = CharField()
    last_name = CharField()
    preferred_name = CharField()
    gender = FixedCharField()
    date_of_birth = DateField()
    institution = CharField()
    tg_user_id = BigIntegerField()
    tg_username = CharField()
    tg_first_name = CharField()
    tg_last_name = CharField()


class Payment(MembershipModel):
    """Payment table representation object"""
    person_id = ForeignKeyField(Person)
    timestamp = DateTimeField()
    amount = DecimalField()
    is_cash = BooleanField(default=False)


class Email(PeopleModel):
    """Email table representation object"""
    person_id = ForeignKeyField(Person)
    email = CharField()


class PhoneNumber(PeopleModel):
    """Phone number table representation object"""
    person_id = ForeignKeyField(Person)
    phone_number = CharField()
    comment = CharField()
    tg_verified = BooleanField()

    # может нужно, а может и нет
    # class Meta:
    #     table_name = "phone_number"


class Event(EventModel):
    """Event table representation object"""
    id = PrimaryKeyField()
    name = CharField()
    place = CharField()
    timestamp = DateTimeField()
    description = TextField()
    coronacheck = BooleanField()
    number_of_people = SmallIntegerField()
    additional_text = TextField()


class Rate(EventModel):
    """Rate table representation object"""
    id = PrimaryKeyField()
    event_id = ForeignKeyField(Event)
    name = CharField()
    description = TextField()
    price = DecimalField()
    member_only = BooleanField()


class Registration(EventModel):
    """Registration table representation object"""
    rate_id = ForeignKeyField(Rate)
    person_id = ForeignKeyField(Person)
    registered = DateTimeField()
    is_payed = BooleanField()
