import os

os.system('cmd /c "pip install ttkbootstrap"')
os.system('cmd /c "pip install requests"')
#os.system('cmd /c "pip install pyllamacpp"')

import tkinter as tk
import ttkbootstrap as ttk
import threading
import requests
#from huggingface_hub import hf_hub_download
#from pyllamacpp.model import Model


class script():
    def juno():    # JUst NOthing
        pass

    def install_and_download():
        accept_button.configure(command=script.juno, text='Installing...')
        license_text.configure(state='normal')
        license_text.delete('1.0', 'end')
        license_text.insert('end', 'Installing Libraries...')


        url_l = 'https://thelecraft999.github.io/JARVIS/latest/temp.txt'
        destination_l = f'{os.path.dirname(os.path.realpath(__file__))}/temp.txt'

        response = requests.get(url_l)
    
        if response.status_code == 200:
            with open(destination_l, 'wb') as file:
                file.write(response.content)
        try:
            with open(destination_l, 'r') as file:
                for line in file:
                    os.system(f'cmd /c "pip install {line.strip().lower()}"')

                    license_text.configure(state='normal')	
                    license_text.insert('end', f'\nSuccessfully installed "{line.strip()}"')
                    license_text.configure(state='disabled')
        except FileNotFoundError:
            print(f"File not found: {destination_l}")
        except Exception as e:
            print(f"An error occurred: {e}")
        try:
            os.remove(destination_l)
        except FileNotFoundError:
            print(f"File not found: {destination_l}")
        except Exception as e:
            print(f"An error occurred: {e}")


        license_text.configure(state='normal')
        license_text.insert('end', '\n\nSuccessfully installed necessary Libraries\n\n------------------------------\n\n')
        license_text.insert('end', 'Downloading necessary files...\n')
        license_text.insert('end', '\n\nDownloading Main-Build...')
        license_text.configure(state='disabled')

        response = requests.get('https://thelecraft999.github.io/JARVIS/latest/jarvis.py')
            
        if response.status_code == 200:
                with open(f'{os.path.dirname(os.path.realpath(__file__))}/jarvis.py', 'wb') as file:
                    file.write(response.content)
                license_text.insert('end', '\n\nDownloading Main-Build')
        else:
                print(f"Failed to download file. Status code: {response.status_code}")
        


        license_text.configure(state='normal')
        license_text.insert('end', '\nSuccessfully downloaded Main-Build\n')
        license_text.insert('end', 'Successfully donwloaded necessary files')
        license_text.insert('end', '\n\nInstallation complete')
        license_text.configure(state='disabled')

        accept_button.configure(command=script.juno, text='Installed')



if __name__ == '__main__':

    root = ttk.Window(themename='darkly')
    root.title('JARVIS Installer -- 1.4')
    root.geometry('700x650')


    title_label = ttk.Label(master=root,
                                    text='JARVIS Installer',
                                    font='Calibri 24 bold')
            
            
    license_frame = ttk.Frame(master= root)
    bottom_label = ttk.Label(master=license_frame,
                                    text='If you click "accept" you accpet our Terms of Use and our End User License Agreement (EULA)',
                                    font='Calibri 8')
            
    license_text = tk.Text(root, state='normal', width=80, height=20)
    license_text.configure(state='normal')
    license_text.insert('end', '''
    Terms of Use / End User License Agreement

    1. DONT COPY THE APP OR OTHER CONTENT published by ThaliumZ-Studios or TheLeCraft999

    2. DONT PASS OF ANY PRODUCT published by ThaliumZ-Studios or TheLeCraft999 AS YOURS

    3.  /

    4.  /

    5.  / 

    6.  /

    7.  /

    8.  /
            ''')
    license_text.configure(state='disabled')

    information_frame = ttk.Frame(master= root)
    password_entry = ttk.Entry(master=information_frame)
    city_entry = ttk.Entry(master=information_frame)
    api_key_entry = ttk.Entry(master=information_frame)


    contact_information = tk.Label(text='''Contact Information:
    Email: thelecraft999@gmail.com
    Discord: thelecraft999
    Discord-Server: https://discord.gg/J8Gzm7nTMP''')
            
    information = tk.Label(text='Note:\nInstalation can take a moment\nYou will automatically download the latest version')
            

    controlbutton_frame = ttk.Frame(master = root)
    cancel_button = ttk.Button(master=controlbutton_frame,
                                text='Cancel',
                                command=quit)
    accept_button = ttk.Button(master=controlbutton_frame,
                                text='Accept & Install',
                                command=threading.Thread(target=script.install_and_download).start)


    title_label.pack()
    bottom_label.pack()
    license_text.pack()
    license_frame.pack()
    information_frame.pack()
    contact_information.pack(pady=13)
    information.pack(pady=5)
    controlbutton_frame.pack()
    accept_button.pack(side='right')
    cancel_button.pack(side='right')



    root.mainloop()