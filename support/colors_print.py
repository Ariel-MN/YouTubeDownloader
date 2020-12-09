from sys import platform as sysPlatform
from os import system, name as osName
import platform

color = True
machine=sysPlatform
checkplatform=platform.platform()
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    color=False
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    color = True
    system('')
if not color:
    white = green = red = yellow = ''
else:
    white, green, red, yellow, blue = '\033[97m', '\033[92m', '\033[91m', '\033[93m', '\033[94m'

# Clearing screen
def ClrScrn():
	  system('cls' if osName == 'nt' else 'clear')

# Banner of the program
def banner(version):
    ClrScrn()
    print(f'''
    {white}__   __       {red} _____     _         {blue}______                    _                _ 
    {white}\ \ / /       {red}|_   _|   | |        {blue}|  _  \                  | |              | |
     {white}\ V /___  _   _{red}| |_   _| |__   ___{blue}| | | |_____      ___ __ | | ___  ____  __| |
      {white}| |/ _ \| | | {red}| | | | | '_ \ / _ \{blue} | | / _ \ \ /\ / / '_ \| |/ _ \ __\ \/ _' |
      {white}| | (_) | |_| {red}| | |_| | |_) |  __/{blue} |/ / (_) \ V  V /| | | | | (_)/ (_| | (_| |
      {white}\_/\___/ \__,_{red}\_/\__,_|_.__/ \___{blue}|___/ \___/ \_/\_/ |_| |_|_|\___\___._|\__._|  {yellow}{version}
    

      {red}Type an {blue}url {red}or {yellow}help {red}for view all the options, {yellow}q {red}for exit.
    ''')

# Creator of the program
def creator(author,email,website):
    print(f"""
      {green}Creator : {white}{author}
      {green}E-mail  : {white}{email}
      {green}Website : {blue}{website}""")

# Help and usage of the program
def help ():
    print(
f"""{green}
{green}Usage:
  {blue}url               {green}If no option is specified, download the video in the best
                    available quality.
  {blue}url {yellow}[option]      {green}A maximum of two options.

{green}Basic Options:
  {yellow} h, help          {green}Show this help.
  {yellow} c, creator       {green}Show information about the creator.
  {yellow} q, quit          {green}Exit the program.
  {yellow} e, exit          {green}Exit the program.

{green}General Options:
  {yellow}-l, --low         {green}Download videos in the lowest quality.
  {yellow}-b, --best        {green}Download videos in the best quality.
  {yellow}-a, --audio       {green}Convert to audio after downloading the video in low quality.
                    The video will be automatically deleted if a quality option
                    or tag is not specified, {green}usage example: {blue}url {yellow}-a {green}or {blue}url {yellow}-b -a

{green}Advanced Options:
  {yellow}-i, --inspect     {green}Inspect the video and show all the available tag numbers.
  {yellow}-t, --tag         {green}Specify the tag number of the video quality to download,
                    {green}usage example: {blue}url {yellow}-t 18 {green}or {blue}url {yellow}-t 18 --audio""")
