import boto3
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from datetime import datetime
import pick


class UserModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = "dynamodb-user"
    username = UnicodeAttribute(hash_key=True)
    #last_updated = UTCDateTimeAttribute()
    #created = UTCDateTimeAttribute(default=datetime.now)


class PickModel(Model):
    class Meta:
        table_name = "dynamodb-pick"
    username = UnicodeAttribute()
    pick = UnicodeAttribute(hash_key=True)
    home = UnicodeAttribute()
    away = UnicodeAttribute()
    favorite = UnicodeAttribute()
    line = NumberAttribute(default=0)
    ou = NumberAttribute(default=0)
    week = NumberAttribute(default=0)
    pick_type = UnicodeAttribute()
    outcome = UnicodeAttribute(default='UNDECIDED')

def create_user_table():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1)

def create_pick_table():
    PickModel.create_table(read_capacity_units=1, write_capacity_units=1)

def get_user(username):
    try:
        user = UserModel.get(username)
        print('username: ' + user.username)
    except UserModel.DoesNotExist:
        print("User does not exist")


def insert_pick(username: str, pick: pick.Pick):
    pick_record = PickModel(pick.pick)
    pick_record.username = username
    pick_record.home = pick.home
    pick_record.away = pick.away
    pick_record.favorite = pick.favorite
    pick_record.line = pick.line
    pick_record.ou = pick.ou
    pick_record.week = pick.week
    pick_record.pick_type = pick.pick_type
    pick_record.outcome = pick.outcome
    pick_record.save()


def pick_record_to_pick_object(pick_record: PickModel):
    return pick.Pick(
        pick=pick_record.pick,
        home=pick_record.home,
        away=pick_record.away,
        week=pick_record.week,
        favorite=pick_record.favorite,
        line=pick_record.line,
        ou=pick_record.ou,
        pick_type=pick_record.pick_type,
        outcome=pick_record.outcome
    )


def get_weeks_available(username):
    weeks_available = set()
    for item in PickModel.scan(PickModel.username == username):
        weeks_available.add(item.week)
    return weeks_available

def get_picks_for_user_for_week(username, week):
    picks = []

    for item in PickModel.scan(PickModel.username.is_in(username) & (PickModel.week == week)):
        picks.append(pick_record_to_pick_object(item))


    print('picks: ' + picks[0].pick_string)
    return picks




