from abdieapp import app
from flask.signals import Namespace

app_signal=Namespace()


""" signals for email notifications on activities"""
coaching_signal = app_signal.signal('coaching')
bookappointment_signal = app_signal.signal('bookappointment')
