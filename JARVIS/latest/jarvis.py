# -- Imports --
import pyaudio                          #/>pip install PyAudio
import speech_recognition as sr         #/>pip install SpeechRecognition
import pyttsx3                          #/>pip install pyttsx3
import pvporcupine                      #/>pip install pvporcupine==1.9.5 
from art import tprint                  #/>pip install art
from bs4 import BeautifulSoup           #/>pip install bs4
from colorama import init as cl_init    #/>pip install colorama
from colorama import Fore               #/>pip install colorama
from colorama import Style              #/>pip install colorama
import os                               #Already installed
import requests                         #Already installed
import datetime as dt                   #Already installed
import struct                           #Already installed
import time                             #Already installed
import hashlib                          #Already installed
import importlib                        #Already installed
import time                             #Already installed
import shutil                           #Already installed

# -- Script --
SKIP_PW = False
cl_init()

def checkcommand():
    while True:
        userSaid = takecommand()
        module_name, command_name = get_config_command(userSaid)
        if dev_mode == 'True':
            print(f'{Fore.LIGHTBLACK_EX}[{Fore.RED}DEV-MODE{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} Module-Name: {module_name}, Command-Name: {command_name}')
        if module_name and command_name:
            if '(' in command_name and ')' in command_name:
                new_command_name = command_name.split('(')[0].strip()
                if dev_mode == 'True':
                    print(f'{Fore.LIGHTBLACK_EX}[{Fore.RED}DEV-MODE{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} Old Command-Name: {command_name}, New Command-Name: {new_command_name}')
                if hasattr(loaded_modules[module_name], new_command_name):
                    function_to_execute = getattr(loaded_modules[module_name], new_command_name)
                    start_index = command_name.find("(")
                    end_index = command_name.find(")")
                    if start_index != -1 and end_index != -1:
                                text_between_parentheses = command_name[start_index + 1:end_index].strip()
                                function_to_execute(eval(text_between_parentheses))
                else:
                    print(f"The function {command_name} does not exist.")
            else:
                if hasattr(loaded_modules[module_name], command_name):
                    function_to_execute = getattr(loaded_modules[module_name], command_name)
                    function_to_execute()
                else:
                    print(f"The function {command_name} does not exist.")
        if 'logout' in userSaid:
             lock()
        if 'log out' in userSaid:
             lock()
        if 'quit' in userSaid:
            quit()
        main()


def takecommand():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as mic:
            print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Listening...')
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print()
            print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Spoken: {Fore.GREEN}{text}{Style.RESET_ALL}')
            return text  
    except:
        if dev_mode == 'True':
            print(f'{Fore.LIGHTBLACK_EX}[{Fore.RED}DEV-MODE{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} ERROR in takecommand')
        main()
 

def main():
    print()
    porcupine = None
    pa = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=['jarvis'])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from('h' * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Wakeword detected...')
                checkcommand()
                time.sleep(1)
                main()
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

    
def get_config_command(user_input):
    config_path = f'{os.path.dirname(os.path.realpath(__file__))}/data/config.txt'
    with open(config_path, 'r') as config_file:
        for line in config_file:
            module_name, command_name, command = line.strip().split(';')
            if command in user_input:
                return module_name, command_name

    return None, None


def startup():
    sha256_hash = hashlib.sha256()
    sha256_hash.update('None'.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()

    if os.path.exists(globalvar.DATA_PATH):
            lines = []
            with open(globalvar.DATA_PATH, 'r') as file:
                    for line in file:
                        if line.startswith('password'):
                            read = str(line.strip())
                            substring_after_equal = read.split('=')[1].strip()
                        else:
                            lines.append(line)
    if hashed_string == substring_after_equal:
        print()
        updater()
    else:
        print('')
        password = input('JARVIS is locked! Please type in password: ')
        print('')
        print('--------------------------------------------------------------------------------')
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode('utf-8'))
        hashed_string = sha256_hash.hexdigest()
        if os.path.exists(globalvar.DATA_PATH):
            lines = []
            with open(globalvar.DATA_PATH, 'r') as file:
                    for line in file:
                        if line.startswith('password'):
                            read = str(line.strip())
                            substring_after_equal = read.split('=')[1].strip()
                        else:
                            lines.append(line)
        if hashed_string == substring_after_equal:
            print('')
            print('Access Granted!')
            print('')
            print('--------------------------------------------------------------------------------')
            print()
            updater() 
        else:
            print('')
            print('Access Forbidden! Wrong Password')
            print('')    
            print('--------------------------------------------------------------------------------')
            startup()


def lock():
    print('--------------------------------------------------------------------------------')
    print('')
    password = input('JARVIS is locked! Please type in password: ')
    print('')
    print('--------------------------------------------------------------------------------')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    if os.path.exists(globalvar.DATA_PATH):
            lines = []
            with open(globalvar.DATA_PATH, 'r') as file:
                    for line in file:
                        if line.startswith('password'):
                            read = str(line.strip())
                            substring_after_equal = read.split('=')[1].strip()
                        else:
                            lines.append(line)
    if hashed_string == substring_after_equal:
        print('')
        print('Access Granted!')
        print('')
        print('--------------------------------------------------------------------------------')
        print()
        main()
    else:
        print()
        print('Access Forbidden! Wrong Password')
        print('')    
        print('--------------------------------------------------------------------------------')
        startup()


def updater():
    try:
        url = "https://thelecraft999.github.io/JARVIS/version.html"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            data = soup.find('p', id='myData').get_text()
        else:
            print(f"Failed to check for the current version, please check your Internet-Settings")
            print()
            print('--------------------------------------------------------------------------------')
            quit()
    except:
        print(f"Failed to check for the current version, please check your Internet-Settings")
        print()
        print('--------------------------------------------------------------------------------')
        quit()       
    if data > globalvar.VERSION:
        print(f'You are running an old version! Latest: {Fore.RED}{data}{Style.RESET_ALL}')
        print(f'Click here to download a newer Version: {Fore.LIGHTBLUE_EX}https://thelecraft999.github.io/JARVIS/downloads.html {Style.RESET_ALL}')
        print()
        print('--------------------------------------------------------------------------------')
    else:
        print(f'{Fore.LIGHTGREEN_EX}You are running the latest version!{Style.RESET_ALL}')
        print()
        print('--------------------------------------------------------------------------------')
    main()


def generate_password(pw):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(pw.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    return hashed_string


def firstsetup():
    pw = input(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Set a password (type "None" to skip using a password)\n> ')
    if (pw == None) or (pw == ''):
        print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Password cant be empty')
        firstsetup()
        print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Restart JARVIS to continue')
        time.sleep(5)
        quit()
    voice = input(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Set voice (use a English [US] voice to obtain best experience)\n> ')    
    hashed_pw = generate_password(pw)
    os.mkdir(f'{os.path.dirname(os.path.realpath(__file__))}/data')
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/data.txt', 'w') as file:
        file.write(f'password={hashed_pw}\n')
        file.write(f'voice={voice}\n')
        file.write(f'devmode=False')
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/globalvar.py', 'w') as file:
        file.write('''import os
VERSION = '2.7'
DATA_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(DATA_DIR, "data.txt")
JARVIS_DIR = os.path.dirname(DATA_DIR)
CMDS_DIR = os.path.join(JARVIS_DIR, 'cmds')''')
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/__init__.py', 'w') as file:
        file.close()
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/config.txt', 'w') as file:
        file.close()
    if not os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/cmds'):
        os.mkdir(f'{os.path.dirname(os.path.realpath(__file__))}/cmds')
    if not os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/cmds/__init__.py'):
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/cmds/__init__.py', 'w') as file:
            file.close()


def import_cmds():
    modules = {}
    jarvis_dir = os.path.dirname(os.path.realpath(__file__))
    cmds_dir = os.path.join(jarvis_dir, 'cmds')
    if os.path.exists(cmds_dir) and os.path.isdir(cmds_dir):
        os.chdir(cmds_dir)
        for file_name in os.listdir(cmds_dir):
            if file_name.endswith(".py") and file_name != "__init__.py":
                module_name = file_name[:-3]
                module = importlib.import_module(f'cmds.{module_name}', '.')
                variable_name = f"m{len(modules) + 1}"
                modules[variable_name] = module
        return modules
    else:
        os.mkdir(f'{jarvis_dir}/cmds')
        print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Restart JARVIS to continue')
        time.sleep(5)
        quit()


if __name__ == '__main__':
    if os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/data') or os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/cmds'):
        if not os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/cmds'):
            os.mkdir(f'{os.path.dirname(os.path.realpath(__file__))}/cmds')
            if not os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/cmds/__init__.py'):
                with open(f'{os.path.dirname(os.path.realpath(__file__))}/cmds/__init__.py', 'w') as file:
                    file.close()
        if not os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/cmds'):
            pw = input(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Set a password (type "None" to skip using a password)\n> ')
            if (pw == None) or (pw == ''):
                print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Password cant be empty')
                firstsetup()
                print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Restart JARVIS to continue')
                time.sleep(5)
                quit()
            voice = input(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Set voice (use a English [US] voice to obtain best experience)\n> ')    
            hashed_pw = generate_password(pw)
            os.mkdir(f'{os.path.dirname(os.path.realpath(__file__))}/data')
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/data.txt', 'w') as file:
                file.write(f'password={hashed_pw}\n')
                file.write(f'voice={voice}\n')
                file.write(f'devmode=False')
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/globalvar.py', 'w') as file:
                file.write('''import os
VERSION = '2.7'
DATA_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(DATA_DIR, "data.txt")
JARVIS_DIR = os.path.dirname(DATA_DIR)
CMDS_DIR = os.path.join(JARVIS_DIR, 'cmds')''')
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/__init__.py', 'w') as file:
                file.close()
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/config.txt', 'w') as file:
                file.close()
        if all(os.path.exists(os.path.join(f'{os.path.dirname(os.path.realpath(__file__))}/data', file)) for file in ['__init__.py', 'data.txt', 'globalvar.py', 'config.txt']):
            from data import globalvar

            if not os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/cmds/__init__.py'):
                print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} {Fore.RED}Corrupted files found{Style.RESET_ALL}')
                with open(f'{os.path.dirname(os.path.realpath(__file__))}/cmds/__init__.py', 'w') as file:
                    file.close()
                print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}Corrupted files repaired{Style.RESET_ALL}')
                print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Restart JARVIS to continue')
                time.sleep(5)
                quit()
            loaded_modules = import_cmds()
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/data.txt', 'r') as file:
                    for line in file:
                        if line.startswith("devmode="):
                            dev_mode = line[len("devmode="):].strip()
            if dev_mode == 'True':
                for variable_name, module in loaded_modules.items():
                    print(f"{Fore.LIGHTBLACK_EX}[{Fore.RED}DEV-MODE{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} {variable_name}: {module.__name__}")    
        else:
            counter = 0
            print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} {Fore.RED}Corrupted files found{Style.RESET_ALL}')
            if [file for file in ['__init__.py', 'data.txt', 'globalvar.py', 'config.txt'] if not os.path.exists(os.path.join(f'{os.path.dirname(os.path.realpath(__file__))}/data', file))]:
                while counter < 4:
                    for file_not_found in [file for file in ['__init__.py', 'data.txt', 'globalvar.py', 'config.txt'] if not os.path.exists(os.path.join(f'{os.path.dirname(os.path.realpath(__file__))}/data', file))]:
                        if file_not_found == '__init__.py':
                            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/__init__.py', 'w') as file:
                                file.close()
                        if file_not_found == 'globalvar.py':
                                with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/globalvar.py', 'w') as file:
                                    file.write('''import os
VERSION = '2.7'
DATA_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(DATA_DIR, "data.txt")
JARVIS_DIR = os.path.dirname(DATA_DIR)
CMDS_DIR = os.path.join(JARVIS_DIR, 'cmds')''')
                        if file_not_found == 'data.txt':
                            pw = input(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Set a password (type "None" to skip using a password)\n> ')
                            if (pw == None) or (pw == ''):
                                print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Password cant be empty')
                                quit()
                            voice = input(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Set voice (use a English [US] voice to obtain best experience)\n> ')    
                            hashed_pw = generate_password(pw)
                            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/data.txt', 'w') as file:
                                file.write(f'password={hashed_pw}\n')
                                file.write(f'voice={voice}\n')
                                file.write(f'devmode=False')
                        if file_not_found == 'config.txt':
                            with open(f'{os.path.dirname(os.path.realpath(__file__))}/data/config.txt', 'w') as file:
                                file.close()
                        counter =+ 1
                    print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}Corrupted files repaired{Style.RESET_ALL}')
                    print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Restart JARVIS to continue')
                    time.sleep(5)
                    quit()
    else:
        firstsetup()
        print(f'{Fore.MAGENTA}{dt.datetime.now().strftime("[%H:%M:%S]")}{Style.RESET_ALL} Restart JARVIS to continue')
        time.sleep(5)
        quit()
    with open(globalvar.DATA_PATH, 'r') as file:
                for line in file:
                    if line.startswith("voice="):
                        voice = line[len("voice="):].strip()
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[int(voice)].id)
    if dev_mode == 'True':
        print(f'{Fore.LIGHTBLACK_EX}[{Fore.RED}DEV-MODE{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} Voice loaded')
    tprint('JARVIS')
    print(f'Version: {globalvar.VERSION}')
    print('--------------------------------------------------------------------------------')
    startup()