from pytube import YouTube

def inspect_video(url):
    video = YouTube(url)
    streams1 = video.streams.filter(progressive=True).order_by('resolution').all()
    streams2 = video.streams.filter(only_video=True).order_by('resolution').all()
    streams3 = video.streams.filter(only_audio=True).order_by('abr').all()
    return streams1, streams2, streams3

def download_video_hd(url, path):
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()
    stream.download(path)
    return stream.default_filename

def advance_download(url, tag, path):
    video = YouTube(url)
    stream = video.streams.get_by_itag(tag)
    stream.download(path)
    return stream.default_filename
