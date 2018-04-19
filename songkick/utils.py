from datetime import datetime
from datetime import timedelta


def strToDate(string):
    datetime.strptime(string, "%Y-%m-%d")


def dateToStr(date):
    datetime.strftime(date, "%Y-%m-%d")


def twoDaysBefore(date):
    date = datetime.date(date) - timedelta(days=2)
    return date


def twoDaysAfter(date):
    date = datetime.date(date) + timedelta(days=2)
    return date

