# Advance-Keylogger
This advanced keylogger captures keystrokes, clipboard data, screenshots, webcam pictures and system information/Ip address. After collecting all information, it’ll be sent to an email address every five minutes. Also, will delete all evidence of files that were sent to an email address.

# Purpose
The purpose of creating this program was my growing curiosity about cybersecurity. I first built a simple keylogger and wondered what else could be added to this program. So, I decided to add five more functions to my program.

# How it works
While the program is running, if the user does not hit the escape key every five minutes, the program will grab all the information gathered and send files to an email address. But if they do hit the escape key, the program will run once and be executed. 

# Functions
- show_pressed()
  Gather user keystrokes, create a file and write to a .txt file
  
- show_clipped()
  Gather user clip board, create a file and write to a .txt file
  
- show_system()
  Gather user system information, create a file and write to a .txt file
  
- show_screenshots()
  Gather user screenshot and save screenshot as .jpg
  
- show_webcam()
  Gather user webcam screenshot and save a screenshot as .jpg
  
- capture_audio()
  Gather 15 seconds of audio and save audio as .wav
  
- send_emails()
  Sending files to email address

# Challenges
Challenges I faced were setting up an email address and sending in multiple files. When working with Gmail, they have certain restrictions for third-party apps. I needed to turn on two-step authentication and create an app password to gain access to my email address. For sending in multiple files, I needed to create a list loop through each file and send them to an email address.                                      
