from pytube import Playlist, YouTube 
from flask import flash
import wget

def download_audio(url):
    video = YouTube(url)
    audio = video.streams.get_audio_only()
    down = audio.download('/home/kim0/Desktop')
    YouTube(url, on_complete_callback=True)
    flash('downloaded success', category="success")
    convert_mp3 = down.removesuffix('.mp4')
    mp3 = (convert_mp3 + '.mp3')
    rename(down, mp3)

def download_video(url,quality):
    video = YouTube(url)

    if quality == 'high':
        down_video = video.streams.get_highest_resolution()
    else:
        down_video = video.streams.get_lowest_resolution()

    down = down_video.download('/home/kim0/Desktop')
    YouTube(url, on_complete_callback=True)
    flash('downloaded success', category="success")

def download_thumbnail(url):
    wget.download(url, '/home/kim0/Desktop/img.jpg')
    flash('downloaded success', category="success")