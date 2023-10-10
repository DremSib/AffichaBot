# AffichaBot
Application for the mini-applications contest. The application is a platform for distributing information about upcoming events in your district or region.
The project is written in Python and the Django framework.
This version of the project has many conventions, such as manual data entry into configuration files, etc.

t.me/@wherecanigobot

# Project setup
First you should install Django.

```bash
pip install Django
```

Open the config.py file. Insert the address where the web application will be located inside the quotes.

```bash
WEB_URL = '<URL>'
```

Go to the Affiche Bot/app/main directory and in the views.py file insert your user_id.

```bash
return render(request, 'main/index.html', {'content': database, 'user_id': <USER_ID>})
```

Launch the project online. I used ngrok for this.

```bash
ngrok http 8000
```

```bash
cd app
```

```bash
python3 manage.py runserver
```

Run the bot

```bash
cd ..
```

```bash
python3 main.py
```

# General information

The application is designed to let people know what events are currently happening in their city. The event can be proposed by anyone who is the creator. In order for you to become a creator, follow the following instructions:

```bash
python3 appoint.py
```

Chose action (1 or 2) and enter your user_id.

# Creator's capabilities

You get an “Admin panel” in which you can create your own new events or delete them.

