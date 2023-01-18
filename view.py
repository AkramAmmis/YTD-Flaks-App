from youtube import *
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
    'description' : '',
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

    return redirect(url_for('view.home'))

@view.route('/')
def home():
    return render_template('home.html', title_page = 'Home',
    show_pl = data_playlist['show'],
    show_v = data_video['show'],
    url_pl = data_playlist['url'],
    title_pl = data_playlist['title'],
    views_pl = data_playlist['views'],
    number_videos = data_playlist['number_videos'],
    thumbnail_url_pl = data_playlist['thumbnail_url'],
    #######################
    url = data_video['url'],
    title = data_video['title'],
    views = data_video['views'],
    description = data_video['description'],
    thumbnail_url = data_video['thumbnail_url'] 
    )

@view.route('/down_audio')
def down_audio():
    #download audio
    download_audio(data_video['url'])
    return redirect(url_for('view.home'))

@view.route('/down_high')
def down_high():
    #download
    download_video(data_video['url'], 'high')
    return redirect(url_for('view.home'))

@view.route('/down_low')
def down_low():
    #download 
    download_video(data_video['url'], 'low')
    return redirect(url_for('view.home'))

@view.route('/down_thumbnail')
def down_thumbnail():
    download_thumbnail(data_video['url'])
    return redirect(url_for('view.home'))

############# PlayList #############
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
    return redirect(url_for('view.home'))

@view.route('/playlist')
def playlist():
    videos = []
    urls = []
    try:
        playlist = Playlist(data_playlist['url'])
        videos_url = playlist.video_urls
        for url in videos_url : 
            urls.append(url)
            video = YouTube(url)
            videos.append(video)
    except KeyError:
        flash('pls enter the url!',category='error')
        return redirect(url_for('view.home'))
    return render_template('playlist.html', title_page='PlayList',
    url_pl = data_playlist['url'],
    title_pl = data_playlist['title'],
    views_pl = data_playlist['views'],
    number_videos = data_playlist['number_videos'],
    videos = videos,
    urls = urls
    )
    
@view.route('/down_thumbnail_pl/<path:url>')
def down_thumbnail_pl(url):
    download_thumbnail(url)
    return redirect(url_for('view.playlist'))


@view.route('/down_audio_pl/<path:id_video>')
def down_audio_pl(id_video):
    url_video = (f'https://www.youtube.com/{id_video}')
    download_audio(url_video)
    return redirect(url_for('view.playlist'))


@view.route('/down_low_pl/<path:id_video>')
def down_low_pl(id_video):
        url_video = (f'https://www.youtube.com/{id_video}')
        download_video(url_video, 'low')
        return redirect(url_for('view.playlist'))

@view.route('/down_high_pl/<path:id_video>')
def down_high_pl(id_video):
        url_video = (f'https://www.youtube.com/{id_video}')
        download_video(url_video, 'high')
        return redirect(url_for('view.playlist'))
