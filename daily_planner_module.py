import threading
import time
import schedule
from tts_module import speak
from speech_recognition_module import voice_recognition
from database_module import Database

def ask_daily_tasks():
    speak("What tasks do you plan to do tomorrow?")
    tasks = voice_recognition()
    if tasks:
        db = Database()
        daily_tasks = db.get_collection('daily_tasks')
        tomorrow = time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400))
        daily_tasks.insert_one({'date': tomorrow, 'tasks': tasks, 'completed': False})
        speak("Tasks recorded for tomorrow.")

def check_reminders():
    db = Database()
    daily_tasks = db.get_collection('daily_tasks')
    today = time.strftime("%Y-%m-%d")
    tasks = daily_tasks.find({'date': today, 'completed': False})
    for task in tasks:
        speak(f"Reminder: You have a task - {task['tasks']}")

def list_tasks_for_today():
    db = Database()
    daily_tasks = db.get_collection('daily_tasks')
    today = time.strftime("%Y-%m-%d")
    tasks = daily_tasks.find({'date': today})
    task_list = list(tasks)
    if task_list:
        response = "Your tasks for today are:\n"
        for task in task_list:
            status = "completed" if task['completed'] else "not completed"
            response += f"{task['tasks']} - {status}\n"
        return response
    return "You have no tasks for today."

def mark_task_completed(task_desc):
    db = Database()
    daily_tasks = db.get_collection('daily_tasks')
    today = time.strftime("%Y-%m-%d")
    result = daily_tasks.update_one({'date': today, 'tasks': task_desc}, {'$set': {'completed': True}})
    if result.modified_count > 0:
        return f"Marked task '{task_desc}' as completed."
    return f"Could not find task '{task_desc}' for today."

# Schedule daily tasks and reminders
schedule.every().day.at("08:00").do(ask_daily_tasks)
schedule.every().minute.do(check_reminders)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()