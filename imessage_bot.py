import pyautogui
import requests
import time
import imessage_config
import messenger_config
import datetime
import os

def short_wait():
    time.sleep(1)

def long_wait():
    time.sleep(3)

def get_contact_list(mode):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    contact_lists = {
        '0': os.path.join(base_dir, 'contact_lists/testing.csv'),
        '1': os.path.join(base_dir, 'contact_lists/main.csv'),
        '2': os.path.join(base_dir, 'contact_lists/vip.csv'),
        '3': os.path.join(base_dir, 'contact_lists/facebook.csv')
    }
    if mode not in contact_lists:
        print(f"Invalid mode: {mode}. Please select a valid mode.")
        return None
    return contact_lists.get(mode)

def mode_select():
    mode = input("""Would you like to send a message to?
    Press 0 for TESTING CONTACT LIST
    Press 1 for MAIN CONTACT LIST
    Press 2 for VIP CONTACT LIST
    Press 3 for FACEBOOK CONTACT LIST
    """)
    return mode

def config_select():
    config = input("""Would you like to send a message to?
    Press 0 for iMessage
    Press 1 for Messenger
    """)
    if config == '0':
        return imessage_config
    elif config == '1':
        return messenger_config
    return config

def ping(msg):
    try:
        requests.post(
            "https://relayproxy.vercel.app/das_record_slack",
            json={"text": msg},
            headers={"Content-Type": "application/json"}
        )
    except requests.RequestException:
        pass
    print("________________________________")
    print(msg)

def text_blast(name, number, message, config):
    # if mouse is moved to the top left corner, the program will stop
    if pyautogui.position() == (0,0):
        ping("iMessage Bot interrupted")
        exit()
    
    if config == imessage_config:
        # if not in safe_mode, the message will be sent
        if imessage_config.safe_mode == False:
            pyautogui.click(imessage_config.new_message_box)
            short_wait()
            pyautogui.click(imessage_config.recipient_box)
            short_wait()
            pyautogui.write(str(number))
            short_wait()
            pyautogui.press('enter')
            short_wait()
            pyautogui.press('enter')
            short_wait()
            pyautogui.typewrite(message)
        else:
            print('SAFE MODE: Message not sent to ', name, 'at ', number)
            return False
    elif config == messenger_config:
        if messenger_config.safe_mode == False:
            pyautogui.click(messenger_config.new_message_box)
            short_wait()
            pyautogui.click(messenger_config.recipient_box)
            short_wait()
            pyautogui.write(name)
            short_wait()
            pyautogui.press('enter')
            short_wait()
            pyautogui.press('enter')
            short_wait()
            pyautogui.typewrite(message)
        else:
            print('SAFE MODE: Message not sent to ', name)
            return False
    return True

def main(contact_list, config):
    if not os.path.exists(contact_list):
        print(f"Error: The file {contact_list} does not exist.")
        return

    with open(contact_list) as f:
        # skip the first line
        f.readline()
        lines = f.readlines()
        for line in lines:
            name = line.split(',')[0].split(' ')[0]
            number = line.split(',')[1] if config == imessage_config else None
            formatted_message = config.message_template.format(name=name)
            if text_blast(name, number, formatted_message, config):
                with open('just_sent.csv', 'a') as f:
                    f.write(name + ',' + (number if number else 'N/A') + ',' + str(datetime.datetime.now()) + '\n')

if __name__ == "__main__":
    mode = mode_select()
    contact_list = get_contact_list(mode)
    if contact_list:
        config = config_select()
        main(contact_list, config)