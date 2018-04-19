from datetime import datetime
from datetime import timedelta


def strToDate(string):
    return datetime.strptime(string, "%Y-%m-%d")


def dateToStr(date):
    return datetime.strftime(date, "%Y-%m-%d")


def dayBefore(strdate):
    date = strToDate(strdate) - timedelta(days=1)
    return dateToStr(date)


def dayAfter(strdate):
    date = strToDate(strdate) + timedelta(days=1)
    return dateToStr(date)
