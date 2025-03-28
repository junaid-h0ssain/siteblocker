import time
import datetime

# Path to the hosts file
HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"  # Windows
# HOSTS_FILE = "/etc/hosts"  # Uncomment for Linux/Mac

REDIRECT_IP = "127.0.0.1"
BLOCKED_SITES = ["www.facebook.com", "facebook.com",
                  "www.youtube.com", "youtube.com",
                  "reddit.com","www.reddit.com",]

BLOCK_DURATION = 20 * 60  # 20 minutes
WAIT_DURATION = 2 * 60 * 60  # 3 hours

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
    print("Blocking websites...")
    modify_hosts(block=True)

def unblock_websites():
    print("Unblocking websites...")
    modify_hosts(block=False)

while True:
    unblock_websites()
    y = 20
    while y>0:
        print(f"Blocked. Next unblock at {datetime.datetime.now() +( datetime.timedelta(y))} {y} minutes left")
        y=y-1
        time.sleep(60)
    #print(f"Unblocked. Next block at {datetime.datetime.now() + datetime.timedelta(minutes=20)}")
    #time.sleep(BLOCK_DURATION)  # Allow 20 minutes

    block_websites()
    x = 120
    while x>0:
        print(f"Blocked. Next unblock at {datetime.datetime.now() +( datetime.timedelta(x))} {x} minutes left")
        x=x-1
        time.sleep(60)
    #time.sleep(WAIT_DURATION)  # Wait 3 hours