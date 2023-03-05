"""
Interweave view functions and middleware to Slack events.

Slack events are: messages, commands, actions, view submissions, etc.
"""

from valet.modules.bot import middleware, views
from valet.modules.bot.app import app

app.command('/parking')(views.command_parking)

app.event(event='app_home_opened')(views.update_home_tab)

app.action('cancel_request')(views.handle_cancel_request)

app.action('actionId-0')(views.handle_datepicker)

app.action('actionId-1')(views.handle_datepicker)

app.middleware(middleware.insert_db_engine)
