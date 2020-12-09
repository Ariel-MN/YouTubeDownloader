from pytube import YouTube
from os import path as osPath

def check_file(filePath, fileName):
    if osPath.exists(osPath.join(filePath, fileName)):
        numb = 1
        while True:
            newName = "{0}_{2}{1}".format(*osPath.splitext(fileName) + (numb,))
            if osPath.exists(osPath.join(filePath, newName)):
                numb += 1
            else:
                return newName
    return fileName

def inspect_video(url):
    video = YouTube(url)
    streams1 = video.streams.filter(progressive=True).order_by('resolution').all()
    streams2 = video.streams.filter(only_video=True).order_by('resolution').all()
    streams3 = video.streams.filter(only_audio=True).order_by('abr').all()
    return streams1, streams2, streams3

def download_video_hd(url, path):
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()
    filename = check_file(path, stream.default_filename)
    name = osPath.splitext(filename) # remove extension
    stream.download(path, filename=name[0])
    return filename

def advance_download(url, tag, path):
    video = YouTube(url)
    stream = video.streams.get_by_itag(tag)
    filename = check_file(path, stream.default_filename)
    name = osPath.splitext(filename) # remove extension
    stream.download(path, filename=name[0])
    return filename
