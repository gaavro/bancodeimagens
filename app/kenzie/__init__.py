import os

def set_directories():
    if os.path.exists('./files_directory'):
        pass
    else:
        os.system('mkdir files_directory')
        os.system('mkdir ./files_directory/gif')
        os.system('mkdir ./files_directory/jpg')
        os.system('mkdir ./files_directory/png')