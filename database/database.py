import sqlite3

# Database connection (database.db)
database = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = database.cursor()

# ---------------- Tables ----------------

# Database initialisation ()
def db_start():

    # Create users table 
    # users (
    # user_id               INT     user ID (Telegram user_id)
    # user_event_counter    INT     event counter
    # user_location         TEXT    user's country and city
    # user_tags             TEXT    user tags
    # user_capabilities     TEXT    can be represented as null, admin and creator
    # )
    cursor.execute('''CREATE TABLE IF NOT EXISTS users ( 
                        user_id INTEGER PRIMARY KEY,
                        user_event_counter INTEGER,
                        user_location TEXT,
                        user_tags TEXT,
                        user_capabilities TEXT
                    )''')
    
    # Create events table
    # events (
    # event_id             INT     event ID
    # event_name           TEXT    event name
    # event_discription    TEXT    event discription
    # event_date           TEXT    event date
    # event_tags           TEXT    event tags
    # event_members        INT     event members  
    # event_owner_id       INT     ID of the user who created the event
    # )
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_name TEXT,
                        event_discription TEXT,
                        event_date TEXT,
                        event_tags TEXT,
                        event_members INT,
                        event_owner_id INTEGER
                    )''')
    database.commit()

# ---------------- User ----------------

# New user initialisation (user_id)
def record_user_id(user_id):
    user = cursor.execute(f'SELECT * FROM users WHERE user_id == {user_id}').fetchone()
    if not user:
        cursor.execute(f'INSERT INTO users (user_id) VALUES ({user_id})')
        database.commit()

# Record user location (user_id, user_location)
def record_user_location(user_id, user_location):
    cursor.execute(f'UPDATE users SET user_location == "{user_location}" WHERE user_id == {user_id}')
    database.commit()

# Record user tags (user_id, user_tags)
def record_user_tags(user_id, user_tag):
    tags = cursor.execute(f'SELECT * FROM users WHERE user_id == {user_id}').fetchone()
    if not tags[3]:
        cursor.execute(f'UPDATE users SET user_tags == "{user_tag}" WHERE user_id == {user_id}')
    else:
        update = f'{tags[3]} {user_tag}'
        cursor.execute(f'UPDATE users SET user_tags == "{update}" WHERE user_id == {user_id}')
    database.commit()

# Request user data (user_id)
def request_user_data(user_id):
    return cursor.execute('SELECT * FROM users WHERE user_id == {key}'.format(key=user_id)).fetchone()

# Request user event counter (user_id)
def request_user_event_counter(user_id):
    return request_user_data(user_id)[1]

# Request user location (user_id)
def request_user_location(user_id):
    return request_user_data(user_id)[2]

# Request user tags (user_id)
def request_user_tags(user_id):
    return request_user_data(user_id)[3]

# Requesr user capabilities (user_id)
def request_user_capabilities(user_id):
    return request_user_data(user_id)[4]

# Delete user location (user_id)
def delete_user_location (user_id):
    return cursor.execute(f'UPDATE users SET user_location == Null WHERE user_id == {user_id}')

# Delete user tags (user_id)
def delete_user_tags(user_id):
    return cursor.execute(f'UPDATE users SET user_tags == Null WHERE user_id == {user_id}')

# ---------------- Table ----------------

#
def record_event(event_name, event_date, event_disctiption, event_tags, event_owner_id):
    cursor.execute(f'INSERT INTO events (event_name, event_discription, event_date, event_tags, event_owner_id) VALUES ("{event_name}", "{event_disctiption}", "{event_date}", "{event_tags}", "{event_owner_id}")')
    database.commit()

# 
def get_event_name_by_owner(event_owner_id):
    cursor.execute(f'SELECT event_name FROM events WHERE event_owner_id = {event_owner_id}')
    result = cursor.fetchall()
    return [row[0] for row in result]

def get_event_id(event_name, event_owner_id):
    cursor.execute("SELECT event_id FROM events WHERE event_name = ? AND event_owner_id = ?", (event_name, event_owner_id))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def delete_event_by_id(event_id):
    cursor.execute(f'DELETE FROM events WHERE event_id = {event_id}')
    database.commit()

# Database initialisation
db_start()