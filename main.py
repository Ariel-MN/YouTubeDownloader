author = "Ariel Montes Nogueira"
email = "info@montesariel.com"
website = "https://montesariel.com"
version = "v 1.0"

# Import basic modules
from os import system, remove, path as osPath
from os.path import realpath
from urllib3.util import parse_url
from urllib3 import PoolManager
from sys import exit as sysExit 
from time import sleep

# Import created modules
from support.colors_print import *
from support.environment_variable import environment_var
import support.youtube_downloader as yt_download
import support.file_converter as f_converter

# Get the current path of the aplication
FullAppPath = realpath(__file__)

# Url validator
def UrlValidator(url):
    # Validate the url structure
    urlParse = parse_url(url)
    if not urlParse.scheme or not urlParse.host:
        error(f'Insert a valid URL like: {yellow}https://youtube.com')
        return
    # Check if the url exist
    http = PoolManager()
    try:
        response = http.request('HEAD', url, timeout=4.0)
    except Exception:
        try:
            # Check internet connection
            response = http.request('HEAD', 'https://youtube.com', timeout=3.0)
        except Exception:
            error("Check your internet connection")
            return
        error('The URL do not exist')
        return
    if response.status < 400:
        return
    error(f'The URL has returned an error {response.status}')

# Program pause
def cmdPause():
    print(f'\n{green}Press any key to continue . . .')
    system('pause > nul')
    main()

# Display errors
def error(msg):
    print(f'\n{red}{msg}{green}')
    cmdPause()

# Get the download folder path
def get_download_path():
    """Returns the default downloads path for Windows or Linux"""
    if osName == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return osPath.join(path.expanduser('~'), 'downloads')

# Download best quality
def DownloadHD(url, path, msg):
    print(f'\n{yellow}Downloading . . .')
    try:
        filename = yt_download.download_video_hd(url, path)
        print(f'\n{green}Done')
        return filename
    except Exception:
        error(msg=msg)

# Download by tag
def DownloadByTag(url, tag, path, msg):
    print(f'\n{yellow}Downloading . . .')
    try:
        filename = yt_download.advance_download(url=url, tag=tag, path=path)
        print(f'\n{green}Done')
        return filename
    except Exception:
        error(msg=msg)

# Convert to audio
def ConvertToAudio(path, filename):
    print(f'\n{yellow}Converting...{green}')
    try:
        f_converter.convert_to_mp3(osPath.join(path, filename))
    except Exception:
        error("Fail trying to convert the video to mp3")

# Main input of the program
def cmdImput():
    try:
        command = input(f'\n{green}YouTube{white}:{blue}~{white}> {green}').split(' ')
        return command
    except KeyboardInterrupt:
        sysExit()

# Display program banner and version
banner(version)

# Try to add the program to the 'Path' os environment variable
try:
    environment_var(FullAppPath)
except Exception:
    print(f"""\n      {white}Consider running with admin privileges the next time to add the program 
    to the path and be able to run it by typing {green}youtube {white}in the shell.
    """)

# Program main function ☆ﾟ.*･｡ﾟ
def main():

    # The main input of the program
    command = cmdImput()

    # Check if user want help
    if command[0].lower() in ["h", "help"]:
        help()
        return main()

    # Show information about the creator
    if command[0].lower() in ["c", "creator"]:
        creator(author, email, website)
        return main()
    
    # Check if user want to exit
    elif command[0].lower() in ["q", "quit", "e", "exit"]:
        sysExit()

    # Validate URL
    UrlValidator(command[0])

    # Get the download path
    download_path = get_download_path()

    # Try to download the video in the best available quality if an URL was provided without specifying any options
    if len(command) == 1:
        url = command[0]
        DownloadHD(url=url, path=download_path, msg="Could not find the video in the given URL")

    # Check commands with an url and one option
    elif len(command) == 2:
        url, option = command
        option.lower()

        # Inspect all available qualities of a video and show them to the user
        if option in ["-i", "--inspect"]:
            try:
                streams1, streams2, streams3 = yt_download.inspect_video(url=url)
            except Exception:
                error("Could not find the video in the given URL")
            if streams1:
                print(f'\n{green}Streams with video and audio:')
                for stream in streams1:
                    print(f'{yellow}{stream}')
            if streams2:
                print(f'\n{green}Streams with video only:')
                for stream in streams2:
                    print(f'{yellow}{stream}')
            if streams3:
                print(f'\n{green}Streams with audio only:')
                for stream in streams3:
                    print(f'{yellow}{stream}')
            return main()

        # Download the video in the lowest quality
        elif option in ["-l", "--low"]:
            DownloadByTag(url=url, tag=18, path=download_path, msg="Could not find the video in the given URL")
        
        # Download the video in the best quality
        elif option in ["-b", "--best"]:
            DownloadHD(url=url, path=download_path, msg="Could not find the video in the given URL")

        # Download the video in low quality and convert it to audio if only the -a option was given
        elif option in ["-a", "--audio"]:
            filename = DownloadByTag(url=url, tag=18, path=download_path, msg="Could not find the video in the given URL")
            ConvertToAudio(path=download_path, filename=filename)
            fileVideo = osPath.join(download_path, filename)
            # Delete the low quality video
            if osPath.exists(fileVideo):
                remove(fileVideo)

    # Check commands with an url and two compatible options or the option --tag and his numeric value
    elif len(command) == 3:
        url, option1, option2 = command
        option1.lower()

        # If the second option is --audio, download the video in the quality given in the first option and then convert it to audio
        if option2.lower() in ["-a", "--audio"]:

            # Download the video in the lowest quality
            if option1 in ["-l", "--low"]:
                filename = DownloadByTag(url=url, tag=18, path=download_path, msg="Could not find the video in the given URL")
            
            # Download the video in the best quality
            elif option1 in ["-b", "--best"]:
                filename = DownloadHD(url=url, path=download_path, msg="Could not find the video in the given URL")
            
            else:
                error(msg="A quality parameter was expected but another was given")

            # Convert the downloaded video in audio
            ConvertToAudio(path=download_path, filename=filename)

        # Download the video quality of the given tag number
        if option1 in ["-t", "--tag"]:
            try:
                tag = int(option2)
            except Exception:
                error("The tag must be an integer")
            DownloadByTag(url=url, tag=tag, path=download_path, msg="Could not find that tag")

    # Download a video by tag and convert it to audio
    elif len(command) == 4:
        url, option1, tag, option2 = command
        option1.lower()
        option2.lower()

        if option1 in ["-t", "--tag"] and option2 in ["-a", "--audio"]:
            try:
                tag = int(tag)
            except Exception:
                error("The tag must be an integer")
            filename = DownloadByTag(url=url, tag=tag, path=download_path, msg="Could not find that tag")
            ConvertToAudio(path=download_path, filename=filename)

        else:
            error("Too many arguments were given")

    # Exceeds the number of allowed parameters
    elif len(command) > 4:
        error("Too many arguments were given")
        
    # Program restarts after completing a task
    sleep(3)
    banner(version)
    return main()

if __name__ == "__main__":        
    # Run the program
    main()
