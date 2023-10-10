from django.db import models
import sqlite3
from datetime import datetime

def restyle_date(date):
    date = str(date)
    return date[6:8] + '/' + date[4:6] + '/' + date[0:4] + ' ' + date[8:10] + ':' + date[10:12]

def request_date():
    current_datetime = datetime.now()
    print(current_datetime)
    return int(str(current_datetime.year) + str(current_datetime.month) + str(current_datetime.day) + str(current_datetime.hour) + str(current_datetime.minute))


def request_database():
    database = sqlite3.connect('../database/database.db')
    cursor = database.cursor()

    query = "SELECT event_id, event_name, event_discription, event_date, event_tags, event_location, event_members FROM events"
    cursor.execute(query)

    rows = cursor.fetchall()

    result = []
    
    for row in rows: 
        print(row[3])
        if row[3] >= request_date():
            result.append(row)

    database.close()

    return result

    
