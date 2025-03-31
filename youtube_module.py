import youtube_dl
import pafy
import pygame
import webbrowser
from database_module import Database

def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info and len(info['entries']) > 0:
            video_id = info['entries'][0]['id']
            return video_id
    return None

def get_audio_url(video_id):
    video = pafy.new(video_id)
    return video.getbestaudio().url

def play_audio(url):
    pygame.mixer.init()
    pygame.mixer.music.load(url)
    pygame.mixer.music.play()

def log_song(song_name, artist="Unknown Artist"):
    db = Database()
    favorite_songs = db.get_collection('favorite_songs')
    favorite_songs.insert_one({'song_name': song_name, 'artist': artist})

def play_youtube_song(song):
    video_id = search_youtube(song)
    if video_id:
        url = get_audio_url(video_id)
        play_audio(url)
        log_song(song)
        return f"Playing {song}."
    return f"Could not find {song} on YouTube."

def open_youtube_video(video_query):
    video_id = search_youtube(video_query)
    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(video_url)
        return f"Opening YouTube video for {video_query}."
    return f"Could not find a YouTube video for {video_query}."