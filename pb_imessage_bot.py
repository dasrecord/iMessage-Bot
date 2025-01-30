import pyautogui
import requests
import time
import config

# imessage_app (180,868)
new_message = (472,50)
to = (560,50)
# message_box = (582,806)

def short_wait():
    time.sleep(1)
def long_wait():
    time.sleep(3)

def get_contact_list(mode):
    contact_lists = {
        '0': '/contact_lists/testing.csv',
        '1': '/contact_lists/main.csv',
        '2': '/contact_lists/vip.csv'
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
        ping("iMessage Bot has been stopped")
        exit()
    pyautogui.click(new_message)
    short_wait()
    pyautogui.click(to)
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

def main(contact_list):
    with open(contact_list) as f:
        lines = f.readlines()
        for line in lines:
            name = line.split(',')[0].split(' ')[0]
            number = line.split(',')[1]
            formatted_message = config.message.format(name=name)
            text_blast(name, number, formatted_message)
            with open('just_sent.csv', 'a') as f:
                f.write(name + ',' + number)
            print("________________________________")
            print('Message sent to: ', name, 'at ', number)

if __name__ == '__main__':
    ping("iMessage Bot is running")
    main(get_contact_list(mode_select()))
    ping("iMessage Bot has finished running")

