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
MY_MAJOR = ""
COMPANY_NAME = ""
JOB_URL = ""
JOB_TITLE = ""
CONNECTION_LIMIT = 20  # Set the limit for connections

MESSAGE_TEMPLATE = """Hi {FirstName}!
My name is {MyFirstName} @ {MySchool} {MyMajor}.
I want to work at {CompanyName}.
Thanks!
"""

# ----------------------------------------------

connections_sent = 0  # Initialize counter


def create_personalized_message(first_name):
    return MESSAGE_TEMPLATE.format(
        FirstName=first_name,
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
    time.sleep(1)

    email_field = driver.find_element(By.ID, "username")
    pass_field = driver.find_element(By.ID, "password")

    email_field.send_keys(LINKEDIN_EMAIL)
    pass_field.send_keys(LINKEDIN_PASSWORD)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(3)


def handle_modal(driver, idx, personalized_message):
    global connections_sent

    try:
        modal = driver.find_element(By.CSS_SELECTOR, "div.artdeco-modal.send-invite")
        add_note_button = modal.find_element(By.CSS_SELECTOR, "button[aria-label='Add a note']")
        add_note_button.click()
        time.sleep(0.5)

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
        time.sleep(0.2)

    except Exception as e:
        print(f"Error while handling modal: {e}")


def send_invites_on_page(driver, search_url):
    global connections_sent

    if connections_sent >= CONNECTION_LIMIT:
        return

    driver.get(search_url)
    time.sleep(3)

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
            time.sleep(0.5)

            first_name = result.find_element(By.CSS_SELECTOR, "a span[aria-hidden='true']").text.split(" ")[0]
            personalized_message = create_personalized_message(first_name)

            handle_modal(driver, idx, personalized_message)

        except Exception as e:
            print(f"Error while processing result {idx}: {e}")


def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        login_to_linkedin(driver)
        print("Login completed!")

        page = 1
        while connections_sent < CONNECTION_LIMIT:
            page_url = BASE_SEARCH_URL + f"&page={page}"
            send_invites_on_page(driver, page_url)
            time.sleep(4)
            print(f"Finished processing page {page}.")
            page += 1

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
