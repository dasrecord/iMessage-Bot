# Configuration file for the iMessage Bot.

# Attributes:
#     message_template (str): Template for the message to be sent. It includes a placeholder for the recipient's name.
#     safe_mode (bool): Flag to enable or disable safe mode.
#     imessage_app (tuple): Coordinates for the iMessage application window.
#     new_message_box (tuple): Coordinates for the 'New Message' button.
#     recipient_box (tuple): Coordinates for the recipient input box.
#     message_box (tuple): Coordinates for the message input box.

message_template = """
Hey, {name}.
Here's my latest video:

"""

safe_mode = True

new_message_box = (110,72)
recipient_box = (200,90)
message_box = (220,822)