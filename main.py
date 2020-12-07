author = "Ariel Montes Nogueira"
email = "info@montesariel.com"
website = "https://montesariel.com"
version = "v 1.0"

# Import basic modules
from os import system, path as osPath
from os.path import realpath
from httplib2 import Http
from time import sleep
from sys import exit

# Import created modules
from support.colors_print import *
from support.environment_variable import environment_var
import support.youtube_downloader as yt_download
import support.file_converter as f_converter

# Get the current path of the aplication
FullAppPath = realpath(__file__)

# Check if url exist
def Check_url(url):
    try:
        h = Http()
        resp = h.request(url, 'HEAD')
    except Exception: return False
    if int(resp[0]['status']) < 400:
        return True
    return False

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
    """Returns the default downloads path for linux or windows"""
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
        command = input(f'{green}YouTube{white}:{blue}~{white}> {green}').split(' ')
        return command
    except KeyboardInterrupt:
        exit()

# Program main function ☆ﾟ.*･｡ﾟ
def main():
    banner(version)

    try:
        environment_var(FullAppPath)
    except Exception:
        print(f"""      {white}Consider running with admin privileges the next time to add the program 
      to the path and be able to run it by typing {green}youtube {white}in the shell.
      """)

    # The main input of the program
    command = cmdImput()

    # Check if user want help
    if command[0].lower() in ["h", "help"]:
        help()        

    # Show information about the creator
    elif command[0].lower() in ["c", "creator"]:
        creator(author, email, website)        

    # Check if user want to exit
    elif command[0].lower() in ["q", "quit", "e", "exit"]:
        exit() 

    # Check if url exist
    if Check_url(command[0]):

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
                print('')
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
                cmdPause()

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
        main()

    # If url do not exist
    else:
        error("The url do not exist")

if __name__ == "__main__":        
    # Run the program
    main()
