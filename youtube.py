from pytube import Playlist, YouTube 
from flask import flash
import wget
from os import path,rename,name,environ
import requests
home_dir = path.expanduser('~')
download_dir = path.join(home_dir, 'Downloads')

def dir_download():
    global download_dir
    if os.name == 'nt':
        download_dir = path.join(os.environ['USERPROFILE'], 'Downloads')
    elif os.name == 'posix':
        download_dir = path.join(os.environ['HOME'], 'Downloads')

def download_audio(url):
    video = YouTube(url)
    audio = video.streams.get_audio_only()
    down = audio.download(download_dir)
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

    down = down_video.download(download_dir)
    YouTube(url, on_complete_callback=True)
    flash('downloaded success', category="success")


def download_thumbnail(url,title):
    img = requests.get(url)
    save_path = path.join(download_dir, f'{title}.jpg')
    with open(save_path , 'wb') as i:
        i.write(img.content)
    flash('downloaded success', category="success")
