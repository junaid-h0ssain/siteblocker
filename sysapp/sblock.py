import time
import datetime
import threading
import pystray
from pystray import MenuItem as item, Icon
from PIL import Image, ImageDraw

# Path to hosts file
HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"  # Windows

REDIRECT_IP = "127.0.0.1"
BLOCKED_SITES = ["www.facebook.com", "facebook.com",
                 "www.youtube.com", "youtube.com",
                 "reddit.com", "www.reddit.com",
                 "www.ndtv.com", "ndtv.com",]

WAIT_DURATION = 10 * 60  # 20 minutes
BLOCK_DURATION = 50 * 60  # 2 hours

is_blocked = False
time_remaining = WAIT_DURATION  # Default start with wait time
icon = None  # Placeholder for system tray icon

with open(HOSTS_FILE, "r+") as file:
    lines = file.readlines()
    file.seek(0)
    for line in lines:
        if not any(site in line for site in BLOCKED_SITES):
            file.write(line)
    file.truncate()

def modify_hosts(block=True):
    with open(HOSTS_FILE, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(site in line for site in BLOCKED_SITES):
                file.write(line)
        if block:
            for site in BLOCKED_SITES:
                file.write(f"{REDIRECT_IP} {site}\n")
        file.truncate()
    


def block_websites():
    global is_blocked, time_remaining
    modify_hosts(block=True)
    is_blocked = True
    time_remaining = BLOCK_DURATION


def unblock_websites():
    global is_blocked, time_remaining
    modify_hosts(block=False)
    is_blocked = False
    time_remaining = WAIT_DURATION


def countdown():
    global time_remaining, is_blocked
    while True:
        if time_remaining > 0:
            time_remaining -= 1
            update_tray_icon()
        else:
            if is_blocked:
                unblock_websites()
            else:
                block_websites()
        time.sleep(1)


def update_tray_icon():
    """Update the tray icon's tooltip with remaining time."""
    if icon:
        mins, secs = divmod(time_remaining, 60)
        status = "Blocked" if is_blocked else "Unblocked"
        icon.title = f"{status} - {mins:02}:{secs:02} remaining"
        icon.icon = create_icon()
        
        

def create_icon():
    """Create an icon for the system tray (Red = Blocked, Green = Unblocked)."""
    img = Image.new("RGB", (64, 64), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    color = (255, 0, 0) if is_blocked else (0, 255, 0)  # Red for blocked, Green for unblocked
    draw.ellipse((10, 10, 54, 54), fill=color)
    return img



def exit_program(icon, item):
    """Exit the program and close the system tray icon."""
    icon.stop()


def run_tray():
    global icon
    menu = (item('Exit', exit_program),)
    icon = Icon("SiteBlocker", create_icon(), menu=menu)
    icon.run()


# Run countdown in a separate thread
countdown_thread = threading.Thread(target=countdown, daemon=True)
countdown_thread.start()

# Run system tray
run_tray()
