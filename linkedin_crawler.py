from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# ---------------- CONFIGURATION ----------------
LINKEDIN_EMAIL = ""  # your linkedin login email
LINKEDIN_PASSWORD = ""  # your linkedin password

# Personalization variables
BASE_SEARCH_URL = ""
MY_FIRST_NAME = ""
MY_LAST_NAME = ""
MY_SCHOOL = ""
MY_MAJOR = "computer science"
COMPANY_NAME = "Microsoft"
JOB_URL = ""
JOB_TITLE = "software developer"
CONNECTION_LIMIT = 1  # Set the limit for connections

# Adjust the speed factor according to your network environment.
# 1: 50mb/s~
# 2: 25mb/s ~ 50mb/s
# 3: ~ 25mb/s
INTERNET_SPEED_FACTOR = 2

# new: send "Add" requests to new people.
# old: send messages to exiting connections.
REQUEST_TYPE = "new"
# REQUEST_TYPE = "old"

# keep it less than 300 words
MESSAGE_TEMPLATE = """
Hi {TheirFirstName}!
My name is {MyFirstName} @ {MySchool} {MyMajor}.
I saw your profile working at {CompanyName}!
How is working at {CompanyName}? I'm looking for a {JobTitle} role.

Thanks!
"""

LONG_MESSAGE_TEMPLATE = """
Hi {TheirFirstName}!
My name is {MyFirstName} @ {MySchool} {MyMajor}. I saw your profile working at {CompanyName}!
How is working at {CompanyName}? I'm looking for a {JobTitle} role.

Also, I would like to get a referral for this position!
{JobUrl}

Thanks!
"""

# ----------------------------------------------

connections_sent = 0  # Initialize counter

def create_personalized_message(their_first_name):
    return MESSAGE_TEMPLATE.format(
        TheirFirstName=their_first_name,
        MyFirstName=MY_FIRST_NAME,
        MyLastName=MY_LAST_NAME,
        MySchool=MY_SCHOOL,
        MyMajor=MY_MAJOR,
        CompanyName=COMPANY_NAME,
        JobUrl=JOB_URL,
        JobTitle=JOB_TITLE,
    )

def create_long_personalized_message(first_name):
    return LONG_MESSAGE_TEMPLATE.format(
        TheirFirstName=first_name,
        MyFirstName=MY_FIRST_NAME,
        MyLastName=MY_LAST_NAME,
        MySchool=MY_SCHOOL,
        MyMajor=MY_MAJOR,
        CompanyName=COMPANY_NAME,
        JobUrl=JOB_URL,
        JobTitle=JOB_TITLE,
    )


def login_to_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(1 * INTERNET_SPEED_FACTOR)

    email_field = driver.find_element(By.ID, "username")
    pass_field = driver.find_element(By.ID, "password")

    email_field.send_keys(LINKEDIN_EMAIL)
    pass_field.send_keys(LINKEDIN_PASSWORD)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(3 * INTERNET_SPEED_FACTOR)


def handle_modal(driver, personalized_message):
    global connections_sent

    try:
        modal = driver.find_element(By.CSS_SELECTOR, "div.artdeco-modal.send-invite")
        add_note_button = modal.find_element(By.CSS_SELECTOR, "button[aria-label='Add a note']")
        add_note_button.click()
        time.sleep(0.5 * INTERNET_SPEED_FACTOR)

        textarea = modal.find_element(By.ID, "custom-message")
        textarea.clear()
        textarea.send_keys(personalized_message)

        send_button = modal.find_element(By.CSS_SELECTOR, "button.artdeco-button--primary")
        if send_button.is_enabled():
            send_button.click()
            connections_sent += 1
            print(f"Invitation sent! Total connections sent: {connections_sent}")
        else:
            print("Send button is disabled.")
        time.sleep(0.2 * INTERNET_SPEED_FACTOR)

    except Exception as e:
        print(f"Error while handling modal: {e}")

def handle_message_modal(driver, personalized_message):
    global connections_sent

    try:
        time.sleep(1 * INTERNET_SPEED_FACTOR)
        
        # Check if a message has already been sent
        existing_message = driver.find_elements(By.CSS_SELECTOR, "div.msg-s-event-with-indicator")
        if existing_message:
            print("A message has already been sent; skipping sending a new one.")
            return

        # Fill out the subject
        subject_input = driver.find_element(By.CSS_SELECTOR, "input[name='subject']")
        subject_input.clear()
        subject_input.send_keys("Hello from UIUC")

        # Enter the personalized message
        message_div = driver.find_element(
            By.CSS_SELECTOR, "div.msg-form__contenteditable[contenteditable='true']"
        )
        message_div.click()
        message_div.send_keys(personalized_message)

        # Locate the send button using the <use> element with href="#send-privately-small"
        send_button = driver.find_element(
            By.XPATH, "//*[name()='use' and @href='#send-privately-small']/ancestor::button"
        )
        
        if send_button.is_enabled():
            send_button.click()
            connections_sent += 1
            print(f"Message sent! Total messages sent: {connections_sent}")
        else:
            print("Send button is disabled.")

        time.sleep(1 * INTERNET_SPEED_FACTOR)
    
    except Exception as e:
        print(f"Error while handling message modal: {e}")

    finally:
        # Close the message modal regardless of what happened above
        try:
            close_button = driver.find_element(By.XPATH, "//*[name()='use' and @href='#close-small']/..")
            close_button.click()
            print("Message modal closed.")
        except Exception as close_err:
            print(f"Could not close modal: {close_err}")


def send_invites_on_page(driver, search_url):
    global connections_sent

    if connections_sent >= CONNECTION_LIMIT:
        return

    driver.get(search_url)
    time.sleep(3 * INTERNET_SPEED_FACTOR)

    results = driver.find_elements(By.CSS_SELECTOR, "div.linked-area.flex-1.cursor-pointer")
    print(f"Found {len(results)} results on page: {search_url}")

    for idx, result in enumerate(results):
        if connections_sent >= CONNECTION_LIMIT:
            print("Connection limit reached. Stopping...")
            return

        try:
            first_child = result.find_element(By.XPATH, "./div")
            children = first_child.find_elements(By.XPATH, "./div")

            if len(children) < 3:
                continue

            button = children[-1].find_element(By.TAG_NAME, "button")

            if "Connect" not in button.text:
                continue

            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", button)
            button.click()
            time.sleep(0.5 * INTERNET_SPEED_FACTOR)

            first_name = result.find_element(By.CSS_SELECTOR, "a span[aria-hidden='true']").text.split(" ")[0]
            personalized_message = create_personalized_message(first_name)

            handle_modal(driver, personalized_message)

        except Exception as e:
            print(f"Error while processing result {idx}: {e}")


def send_messages_on_page(driver, search_url):
    global connections_sent
    if connections_sent >= CONNECTION_LIMIT:
        return

    driver.get(search_url)
    time.sleep(3 * INTERNET_SPEED_FACTOR)

    results = driver.find_elements(By.CSS_SELECTOR, "div.linked-area.flex-1.cursor-pointer")
    print(f"Found {len(results)} results on page: {search_url}")

    for idx, result in enumerate(results):
        if connections_sent >= CONNECTION_LIMIT:
            print("Connection limit reached. Stopping...")
            return
        try:
            first_child = result.find_element(By.XPATH, "./div")
            children = first_child.find_elements(By.XPATH, "./div")
            if len(children) < 3:
                continue
            button = children[-1].find_element(By.TAG_NAME, "button")

            # We look for "Message"
            text_or_aria = button.text.strip() + " " + (button.get_attribute("aria-label") or "")
            if "Message" not in text_or_aria:
                continue

            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", button)
            button.click()
            time.sleep(1 * INTERNET_SPEED_FACTOR)

            # Extract first name
            full_name = result.find_element(By.CSS_SELECTOR, "a span[aria-hidden='true']").text
            first_name = full_name.strip().split(" ")[0]
            personalized_message = create_long_personalized_message(first_name)

            handle_message_modal(driver, personalized_message)

        except Exception as e:
            print(f"Error while processing result {idx}: {e}")


def main(request_type):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        login_to_linkedin(driver)
        print("Login completed!")

        page = 1
        while connections_sent < CONNECTION_LIMIT:
            page_url = BASE_SEARCH_URL + f"&page={page}"
            if request_type == "new":
                send_invites_on_page(driver, page_url)
            elif request_type == "old":
                send_messages_on_page(driver, page_url)
            time.sleep(4 * INTERNET_SPEED_FACTOR)
            print(f"Finished processing page {page}.")
            page += 1

    finally:
        driver.quit()


if __name__ == "__main__":
    main(REQUEST_TYPE)
