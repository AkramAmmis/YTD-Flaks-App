from flask import render_template, redirect, url_for, flash, request , Blueprint
from pytube import YouTube,Playlist
from os import rename
import urllib
import socket
import wget

view = Blueprint('view', __name__)

data_video = {
    'url':'url',
    'title' : '',
    'views' : '',
    'description' : '',
    'thumbnail_url' : '',
    'show' : 'off'
}

data_playlist = {
    'url':'url',
    'title' : '',
    'views' : '',
    'number_videos' : '',
    'thumbnail_url' : '',
    'show' : 'off'
    
}
def internet_test():
    try : 
        socket.create_connection(('youtube.com', 80))
        return True
    except OSError: 
        return False



@view.route('/get_youtube', methods=['POST' ,'GET'])
def get_youtube():
    
    #geting video and informaion about video
    url = request.form.get('url')
    if url:
        if internet_test() == True :
            if 'playlist?list=' not in url:
                try:
                    try:
                        video = YouTube(url)
                    except:
                        url = data_video['url']
                        video = YouTube(url)
                        flash('Pless Enter a valid url', category='error')
                except:
                        flash('Pless Enter a valid url', category='error') 
                else: 
                        data_video['show'] = 'on'
                        data_playlist['show'] = 'of'
                        data_video['url'] = url
                        data_video['title'] = video.title
                        data_video['views'] = video.views
                        data_video['thumbnail_url'] = video.thumbnail_url
                        description = video.description
                        data_video['description'] = " ".join(description.split()[:25])

            else:
                playlist = Playlist(url)
                if playlist:
                    videos = playlist.video_urls
                    url_first_video = videos[0]
                    data_playlist['show'] = 'on'
                    data_video['show'] = 'of'
                    data_playlist['url'] = url
                    data_playlist['thumbnail_url'] = YouTube(url_first_video).thumbnail_url
                    data_playlist['title'] = title_pl = playlist.title
                    data_playlist['number_videos'] = len(playlist)
                    data_playlist['views'] = playlist.views
                else : 
                    flash('Pless Enter a valid url', category='error') 
        else:
                flash('Pless Check if you connect internet!', category='error')

    else :
        flash('Pless Enter Url!', category='error')

    return redirect(url_for('view.down_page'))

@view.route('/')
def down_page():
    return render_template('down_page.html', title_page = 'Download Page',
    show_pl = data_playlist['show'],
    show_v = data_video['show'],
    url_pl = data_playlist['url'],
    title_pl = data_playlist['title'],
    views_pl = data_playlist['views'],
    number_videos = data_playlist['number_videos'],
    thumbnail_url_pl = data_playlist['thumbnail_url'],
    ####
    url = data_video['url'],
    title = data_video['title'],
    views = data_video['views'],
    description = data_video['description'],
    thumbnail_url = data_video['thumbnail_url'] 
    )

@view.route('/down_audio')
def down_audio():
    #download audio
    video = YouTube(data_video['url'])
    audio = video.streams.get_audio_only()
    down = audio.download('/home/kim0/Desktop')
    flash('Start download ... ', category="success")
    YouTube(data_video['url'], on_complete_callback=True)
    flash('downloaded success', category="success")
    #convert to mp3
    convert_mp3 = down.removesuffix('.mp4')
    mp3 = (convert_mp3 + '.mp3')
    rename(down, mp3)
    return redirect(url_for('view.down_page'))

@view.route('/down_high')
def down_high():
    #download
    video = YouTube(data_video['url'])
    down_video = video.streams.get_highest_resolution()
    down = down_video.download('/home/kim0/Desktop')
    YouTube(data_video['url'], on_complete_callback=True)
    flash('downloaded success', category="success")
    return redirect(url_for('view.down_page'))

@view.route('/down_low')
def down_low():
    #download 
    video = YouTube(data_video['url'])
    down_video = video.streams.get_lowest_resolution()
    down = down_video.download('/home/kim0/Desktop')
    YouTube(data_video['url'], on_complete_callback=True)
    flash('downloaded success', category="success")
    return redirect(url_for('view.down_page'))

@view.route('/down_thumbnail')
def down_thumbnail():
    name = data_video['title']
    thumbnail_url = data_video['thumbnail_url']
    wget.download(thumbnail_url, f'/home/kim0/Desktop/{name}.jpg')
    flash('downloaded success', category="success")
    return redirect(url_for('view.down_page'))


@view.route('/down_pl_low')
def down_pl_low():
    playlist = Playlist(data_playlist['url'])
    videos = playlist.video_urls
    for video_url in videos:
        video = YouTube(video_url)
        down_video = video.streams.get_lowest_resolution()
        down = down_video.download('/home/kim0/Desktop')
        YouTube(video_url, on_complete_callback=True)
        flash('downloaded success', category="success")
    return redirect(url_for('view.down_page'))


@view.route('/down_pl_high')
def down_pl_high():
    playlist = Playlist(data_playlist['url'])
    videos = playlist.video_urls
    for video_url in videos:
        video = YouTube(video_url)
        down_video = video.streams.get_highest_resolution()
        down = down_video.download('/home/kim0/Desktop')
        YouTube(video_url, on_complete_callback=True)
        flash('downloaded success', category="success")
    return redirect(url_for('view.down_page'))
