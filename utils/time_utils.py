import datetime
import time


def time_now():
    return time.time()


def get_date_time_since(minutes_ago=0):
    return time_now() - (minutes_ago*60)
