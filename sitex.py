from selenium import webdriver
import time

# List of websites to block
BLOCKED_SITES = ["facebook.com", "youtube.com"]
ALLOW_DURATION = 20 * 60  # 20 minutes
WAIT_DURATION = 3 * 60 * 60  # 3 hours

# Launch Firefox WebDriver
def start_browser():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run in background (optional)
    driver = webdriver.Firefox(options=options)
    return driver

# Check open tabs and close blocked sites
def check_and_close_tabs(driver):
    while True:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            current_url = driver.current_url
            if any(site in current_url for site in BLOCKED_SITES):
                print(f"Closing {current_url}")
                driver.close()
        time.sleep(10)  # Check every 10 seconds

# Main loop
while True:
    print("Blocking sites...")
    driver = start_browser()
    check_and_close_tabs(driver)
    time.sleep(WAIT_DURATION)  # Wait 3 hours

    print("Allowing sites for 20 minutes...")
    time.sleep(ALLOW_DURATION)
