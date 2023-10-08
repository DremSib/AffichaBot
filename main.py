import telebot
from telebot import types 
from database import database
import config
import datetime

# Launch a bot (TOKEN)
bot = telebot.TeleBot(config.TOKEN)

# ---------------- SECONDARY FUNCTIONS ---------------- #

# Determine country and city (latitude, longitude)
# (!) This function is conditional. For its full implementation, a geo API is required.
# (!) For simplicity, it outputs the values ​​of "current_country" and "current_city".
def determine_location(latitude, longitude, GEO_API_KEY=config.GEO_API_KEY):
    return 'current_location'

# Determines whether the date is correct (date)
def is_valide_date(date):
    try:
        if len(date) == 16:
            current_datetime = datetime.datetime.now()
            flag = False
            if int(date[6:10]) >= current_datetime.year:
                if int(date[3:5]) >= current_datetime.month and current_datetime.month <= 12:
                    if int(date[0:2]) > current_datetime.day and current_datetime.day <= 31:       
                        flag = True
            return flag
    except:
        return False

# Determines whether the event name is correct
# (!) Title cannot start with '/'
def is_valide_event_name(name):
    if name[0] == '/':
        return False
    else:
        return True
        

# ---------------- BOT CODE ---------------- #

# Main menu () 
@bot.message_handler(commands=['start'])
def start(message):
    database.record_user_id(message.chat.id)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if not database.request_user_location(message.chat.id):
        button_geolocation_request = types.KeyboardButton('Send where I am', request_location=True)
        markup.add(button_geolocation_request)
    if not database.request_user_tags(message.chat.id):
        button_interests_test = types.KeyboardButton('Take the test')
        markup.add(button_interests_test)
    if database.request_user_capabilities(message.chat.id):
        button_admin_panel = types.KeyboardButton('Admin panel')
        markup.add(button_admin_panel)
    if database.request_user_location(message.chat.id) and database.request_user_tags(message.chat.id):
        button_launch_the_application = types.KeyboardButton('Launch the App')
        button_settings = types.KeyboardButton('Settings')
        markup.add(button_launch_the_application, button_settings)
    if not database.request_user_data(message.chat.id)[2] or not database.request_user_data(message.chat.id)[3]:
        bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name}. Register to get started. Send your location and take a short test.', reply_markup=markup)
    else: 
        bot.send_message(message.chat.id, f'{message.from_user.first_name} you can now launch the application with confidence!', reply_markup=markup)

# Geolocation determination () 
@bot.message_handler(content_types=['location'])
def geolocation_request(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    location = determine_location(latitude, longitude)
    database.record_user_location(message.chat.id, location)
    start(message)

# Interests test ()
@bot.message_handler(func=lambda message: message.text == 'Take the test')
def test(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = [types.KeyboardButton(config.tags[i]) for i in range(len(config.tags))]
    button_exit = types.KeyboardButton('Done')
    markup.add(*buttons).add(button_exit)
    bot.send_message(message.chat.id, 'Choose what you love:', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text in config.tags)
def button_test_click(message):
    if message.text in config.tags:
        database.record_user_tags(message.chat.id, message.text)


# Admin panel ()
@bot.message_handler(func=lambda message: message.text == 'Admin panel')
def admin_panel(message):
    if database.request_user_capabilities(message.chat.id):
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_add_new_event = types.KeyboardButton('Add new event')
        button_delete_event = types.KeyboardButton('Delete event')
        button_exit = types.KeyboardButton('Back')
        markup.add(button_add_new_event, button_delete_event, button_exit)
        bot.send_message(message.chat.id, 'You are in the admin panel', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'You are not admin')
        start(message)

# ---- Add new event ()
@bot.message_handler(func=lambda message: message.text == 'Add new event')
def add_new_event(message):
    event = []
    bot.send_message(message.chat.id, 'Enter event name', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_event_name, event)
def get_event_name(message, event):
    event.append(message.text)
    if is_valide_event_name(event[0]):
        bot.send_message(message.chat.id, 'Enter event date\n\nDD/MM/YYYY HH:MM')
        bot.register_next_step_handler(message, get_event_date, event)
    else:
        bot.send_message(message.chat.id, "Err: title cannot start with '/'")
        admin_panel(message)
def get_event_date(message, event):
    if is_valide_date(message.text) == True:
        bot.send_message(message.chat.id, 'Enter event discription')
        event.append(message.text)
        bot.register_next_step_handler(message, get_event_discription, event)
    else: 
        bot.send_message(message.chat.id, 'Err: incorrect date')
        admin_panel(message)
def get_event_discription(message, event):
    event.append(message.text)
    bot.send_message(message.chat.id, f'Enter event tags from possible tags\n\nPossible tags:\n {config.tags}\n\nExample: Art, Cars')
    bot.register_next_step_handler(message, get_event_tags, event)
def get_event_tags(message, event):
    event.append(message.text)
    bot.send_message(message.chat.id, f'{event[0]}\n\n{event[1]}\n\n{event[2]}\n\n{event[3]}')
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_confirm = types.KeyboardButton('Confirm')
    button_reject = types.KeyboardButton('Reject')
    markup.add(button_confirm, button_reject)
    bot.send_message(message.chat.id, 'Right?', reply_markup=markup)
    bot.register_next_step_handler(message, event_confirm, event)
def event_confirm(message, event):
    if message.text == 'Confirm':
        database.record_event(event[0], event[1], event[2], event[3], message.chat.id)
        bot.send_message(message.chat.id, 'New event was added!')
        admin_panel(message)
    elif message.text == 'Reject':
        bot.send_message(message.chat.id, 'New event was not added')
        admin_panel(message)
    else:
        bot.send_message(message.chat.id, 'Err: event was not added')
        admin_panel(message)

# ---- Delete event ()
@bot.message_handler(func=lambda message: message.text == 'Delete event')
def delete_event(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [types.KeyboardButton(database.get_event_name_by_owner(message.chat.id)[i]) for i in range(len(database.get_event_name_by_owner(message.chat.id)))] 
    button_exit = types.KeyboardButton('Back')
    markup.add(*buttons).add(button_exit)
    bot.send_message(message.chat.id, 'Select which event to delete', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text in database.get_event_name_by_owner(message.chat.id))
def button_delete_click(message):
    if message.text in database.get_event_name_by_owner(message.chat.id):
        database.delete_event_by_id(database.get_event_id(message.text, message.chat.id))
        bot.send_message(message.chat.id, f'You deleted {message.text}')
        admin_panel(message)

# Settings ()
@bot.message_handler(func=lambda message: message.text == 'Settings')
def settings(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_change_location = types.KeyboardButton('Change location', request_location=True)
    button_change_tags = types.KeyboardButton('Change interests')
    button_exit = types.KeyboardButton('Back')
    markup.add(button_change_location, button_change_tags, button_exit)
    bot.send_message(message.chat.id, 'Settings', reply_markup=markup)

# ---- Change location ()
@bot.message_handler(func=lambda message: message.text == 'Change location')
def change_location(message):
    database.delete_user_location(message.chat.id)
    geolocation_request(message)

# ---- Change interests ()
@bot.message_handler(func=lambda message: message.text == 'Change interests')
def change_interests(message):
    database.delete_user_tags(message.chat.id)
    test(message)

# Back to menu ()
@bot.message_handler(func=lambda message: message.text == 'Back' or 'Done')
def back_to_menu(message):
    start(message)

# Polling ()
bot.polling()
