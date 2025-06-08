import os
import sys
import sqlite3
froms datetime import datetime, timedelta
import pytz
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import bot_database as database
from bot_config import TIMEZONE

database.DB_NAME = "test_reminders.db"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    if os.path.exists(database.DB_NAME):
        os.remove(database.DB_NAME)
    database.init_db()
    yield
    if os.path.exists(database.DB_NAME):
        os.remove(database.DB_NAME)

def test_add_and_get_reminder():
    chat_id = 12345
    reminder_time = datetime.now(TIMEZONE) + timedelta(hours=1)
    reminder_text = "Тест"
    database.add_reminder_to_db(chat_id, reminder_time, reminder_text)
    reminders = database.get_pending_reminders(chat_id)
    assert len(reminders) == 1
    rem_id, rem_time_str, rem_text = reminders[0]
    assert rem_text == reminder_text
    rem_time_from_db = pytz.utc.localize(datetime.strptime(rem_time_str, "%Y-%m-%d %H:%M:%S"))
    assert rem_time_from_db.strftime("%Y%m%d%H%M") == reminder_time.astimezone(pytz.utc).strftime("%Y%m%d%H%M")

def test_delete_reminder():
    chat_id = 54321
    reminder_time = datetime.now(TIMEZONE) + timedelta(days=1)
    database.add_reminder_to_db(chat_id, reminder_time, "Видалити")
    reminders_before = database.get_pending_reminders(chat_id)
    assert len(reminders_before) == 1
    reminder_id = reminders_before[0][0]
    database.delete_reminder_from_db(reminder_id)
    reminders_after = database.get_pending_reminders(chat_id)
    assert len(reminders_after) == 0

def test_check_reminders_logic():
    chat_id = 999
    time_past = datetime.now(TIMEZONE) - timedelta(minutes=5)
    database.add_reminder_to_db(chat_id, time_past, "Минуле")
    time_future = datetime.now(TIMEZONE) + timedelta(minutes=5)
    database.add_reminder_to_db(chat_id, time_future, "Майбутнє")
    ready = database.get_all_pending_reminders_for_check()
    assert len(ready) == 1
    assert ready[0][2] == "Минуле"

def test_mark_reminder_sent():
    chat_id = 777
    time_past = datetime.now(TIMEZONE) - timedelta(minutes=1)
    database.add_reminder_to_db(chat_id, time_past, "Відправити")
    ready = database.get_all_pending_reminders_for_check()
    assert len(ready) == 1
    database.mark_reminder_sent(ready[0][0])
    still_ready = database.get_all_pending_reminders_for_check()
    assert len(still_ready) == 0

def test_get_reminders_for_empty_user():
    reminders = database.get_pending_reminders(chat_id=11111)
    assert reminders == []

def test_delete_non_existent_reminder():
    try:
        database.delete_reminder_from_db(99999)
        assert True
    except Exception as e:
        pytest.fail(f"Видалення викликало помилку: {e}")

def test_time_is_stored_in_utc():
    chat_id = 222
    local_time = datetime.now(TIMEZONE) + timedelta(days=5)
    database.add_reminder_to_db(chat_id, local_time, "UTC тест")
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT reminder_time FROM reminders WHERE chat_id = ?", (chat_id,))
    time_str_db = cursor.fetchone()[0]
    conn.close()
    expected_utc_str = local_time.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
    assert time_str_db == expected_utc_str