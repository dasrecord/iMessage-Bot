import pyautogui
import requests
import time
import config
import datetime

def short_wait():
    time.sleep(1)

def long_wait():
    time.sleep(3)

def get_contact_list(mode):
    contact_lists = {
        '0': 'contact_lists/testing.csv',
        '1': 'contact_lists/main.csv',
        '2': 'contact_lists/vip.csv'
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
    """)
    return mode

def ping(msg):
    try:
        requests.post(
            "https://relayproxy.vercel.app/das_record_slack",
            json={"text": msg},
            headers={"Content-Type": "application/json"}
        )
    except requests.RequestException:
        pass
    print(msg)

def text_blast(name, number, message):
    # if mouse is moved to the top right corner, the program will stop
    if pyautogui.position() == (0,0):
        ping("iMessage Bot interrupted")
        exit()
    # if not in safe_mde, the message will be sent
    if config.safe_mode == False:
        pyautogui.click(config.new_message)
        short_wait()
        pyautogui.click(config.to)
        short_wait()
        pyautogui.write(str(number))
        short_wait()
        pyautogui.press('enter')
        short_wait()
        pyautogui.press('enter')
        short_wait()
        pyautogui.write(message,0.01)
        long_wait()
        pyautogui.press('enter')
        short_wait()
        return True
    else:
        print('SAFE MODE: Message not sent to ', name, 'at ', number)
        return False

def main(contact_list):
    with open(contact_list) as f:
        lines = f.readlines()
        for line in lines:
            name = line.split(',')[0].split(' ')[0]
            number = line.split(',')[1]
            formatted_message = config.message_template.format(name=name)
            if text_blast(name, number, formatted_message):
                with open('just_sent.csv', 'a') as f:
                    f.write(name + ',' + number + ',' + str(datetime.datetime.now()) + '\n')
                print("________________________________")
                print('Message sent to: ', name, 'at ', number)

if __name__ == '__main__':
    ping("iMessage Bot started")
    main(get_contact_list(mode_select()))
    ping("iMessage Bot finished")

