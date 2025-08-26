import datetime
from sqlalchemy import func
from abdieapp import db

"""Posting models"""
class Booking(db.Model):
    bk_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    bk_organisation = db.Column(db.String(255), nullable=False)
    bk_fname = db.Column(db.String(255), nullable=False)
    bk_lname = db.Column(db.String(255), nullable=False)
    bk_phone = db.Column(db.String(225), nullable=False)
    bk_email = db.Column(db.String(255), nullable=False)
    bk_message = db.Column(db.Text(), nullable=True)
    bk_budget = db.Column(db.String(255), nullable=False)
    bk_bdate = db.Column(db.DateTime())
    bk_date = db.Column(db.DateTime(), default=datetime.datetime.now())
    bk_duration = db.Column(db.Enum('5 min', '15 min','30 min', '1 hour', '2 hours', '5 hours'), server_default='30 min')
    bk_delete = db.Column(db.Enum('deleted', 'not deleted'), server_default='not deleted')

class Coaching(db.Model):
    ch_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    ch_fullname = db.Column(db.String(255), nullable=False)
    ch_phone = db.Column(db.String(225), nullable=False)
    ch_email = db.Column(db.String(255), nullable=False)
    ch_date = db.Column(db.DateTime(), default=datetime.datetime.now())
    ch_delete = db.Column(db.Enum('deleted', 'not deleted'), server_default='not deleted')