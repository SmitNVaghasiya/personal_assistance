from file_search_module import search_and_open_file
from file_reader_module import read_and_respond_to_file
from youtube_module import play_youtube_song, open_youtube_video
from online_search_module import online_search
from daily_planner_module import list_tasks_for_today, mark_task_completed
from groq_module import groq_response
from tts_module import speak

def handle_command(text):
    if not text:
        return

    text_lower = text.lower()

    # Use Groq to classify the intent for task-related commands
    intent = groq_response(text_lower, intent_recognition=True)

    if intent == "list_tasks":
        response = list_tasks_for_today()
    elif intent == "mark_task":
        task_desc = text_lower.replace("mark task ", "").strip()
        if task_desc:
            response = mark_task_completed(task_desc)
        else:
            response = "Please specify a task to mark as completed."
    elif text_lower.startswith('search for '):
        filename = text_lower[10:].strip()
        if filename:
            response = search_and_open_file(filename)
        else:
            response = "Please specify a filename to search for."
    elif text_lower.startswith('read file '):
        filename = text_lower[10:].strip()
        if filename:
            response = read_and_respond_to_file(filename)
        else:
            response = "Please specify a filename to read."
    elif text_lower.startswith('play '):
        song = text_lower[5:].strip()
        response = play_youtube_song(song)
    elif text_lower.startswith('open youtube video '):
        video_query = text_lower[19:].strip()
        response = open_youtube_video(video_query)
    elif text_lower.startswith('search online for '):
        query = text_lower[18:].strip()
        response = online_search(query)
    else:
        response = groq_response(text)

    speak(response)