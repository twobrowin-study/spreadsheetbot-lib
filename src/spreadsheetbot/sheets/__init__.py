from spreadsheetbot.sheets.i18n import I18n
from spreadsheetbot.sheets.switch import Switch
from spreadsheetbot.sheets.settings import Settings
from spreadsheetbot.sheets.registration import Registration
from spreadsheetbot.sheets.log import LogSheet
from spreadsheetbot.sheets.groups import Groups
from spreadsheetbot.sheets.users import Users
from spreadsheetbot.sheets.report import Report
from spreadsheetbot.sheets.keyboard import Keyboard
from spreadsheetbot.sheets.notifications import Notifications

import asyncio
from telegram.ext import Application
from telegram.constants import ParseMode

from spreadsheetbot.basic.log import Log

def PerformAndScheldueNotifications(app: Application):
    app.create_task(
        _perform_notifications(app),
        {
            'action': 'Perform first notifications'
        }
    )
    ScheldueNotifications(app)

def ScheldueNotifications(app: Application) -> None:
    app.create_task(
        _scheldue_and_perform_notification(app),
        {
            'action': 'Perform scheldued notifications'
        }
    )

async def _scheldue_and_perform_notification(app: Application) -> None:
    await asyncio.sleep(Settings.notifications_update_time)
    ScheldueNotifications(app)
    await _perform_notifications(app)

async def _perform_notifications(app: Application) -> None:
    Log.info("Start performing notification")
    for idx,row in Notifications.as_df.loc[Notifications.selector_to_notify()].iterrows():
        Users.send_notification_to_all_users(
            app, row.text_markdown, ParseMode.MARKDOWN, row.send_picture, row.state, row.condition
        )
        if row.state == "":
            Groups.send_to_all_normal_groups(app, row.text_markdown, ParseMode.MARKDOWN, row.send_picture)
        admin_group_text = \
            Settings.notification_admin_groups_template.format(message=row.text_markdown) if row.condition == None \
            else Settings.notification_admin_groups_condition_template.format(message=row.text_markdown, condition=row.condition)
        Groups.send_to_all_admin_groups(
            app, 
            admin_group_text,
            ParseMode.MARKDOWN,
            row.send_picture
        )
        await Notifications.set_done(idx)
    Log.info("Done performing notification")