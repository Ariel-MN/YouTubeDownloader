# Import basic modules
from os import listdir, name as osName, path as osPath
from winreg import CreateKey, CloseKey, HKEY_LOCAL_MACHINE, QueryValueEx, SetValueEx, REG_SZ

# Import created modules
from support.colors_print import white, green

# Create environment variable for call the program from shell, only works with compiled version
def environment_var(FullPath):

    def add_var(path):
        # Add the variable
        SetValueEx(key, 'Path', 0, REG_SZ, path)
        CloseKey(key)
        print(f"""      {white}The app has been added to the path, after reboot you can run it by 
      typing {green}youtube {white}in the shell.
      """)

    # Get the current path of the aplication
    AppPath = f'{FullPath}'.replace('main.py', '')
    FullAppPath = FullPath.lower()
    
    # Controls that a compiled program exists in the app path
    if any(File.endswith('.exe') for File in listdir(AppPath)):

        # These are the application directories when the program is run from cmd
        runFromCMD = [
            osPath.join(osPath.expandvars(r"%WINDIR%"), 'System32\main.py').lower(),  # path when runing with admin permissions
            osPath.join(osPath.expandvars(r"%userprofile%"), 'main.py').lower()       # path when runing without admin permissions
        ]
        
        # Check that is runing on Windows and that it is not being called from cmd already
        if osName == 'nt' and FullAppPath not in runFromCMD:

            # Point to the registry key of the system environment variables
            key = CreateKey(HKEY_LOCAL_MACHINE, r'System\CurrentControlSet\Control\Session Manager\Environment')

            try:
                # Try to get the value of the Path variable
                allPaths = QueryValueEx(key, 'Path')[0]
            except Exception:
                # Create the Path variable if it doesn't exist
                add_var(path=AppPath)
                return        
            
            # Get all the values of the existing paths
            Path=allPaths.split(';')

            # If the Path is empty, add the application path
            if Path == ['']:
                add_var(path=AppPath)
                return

            # Check if the application path is in the Path variable
            if AppPath not in Path:
                # Add the application path to the Path environment variable and add keep the others existing paths
                add_var(path=AppPath+';'+allPaths)
