from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

# ---------------- CONFIGURATION ----------------
LINKEDIN_EMAIL = "" # your linkedin login email
LINKEDIN_PASSWORD = "" # your linkedin password


# Personalization variables
BASE_SEARCH_URL = ""
MY_FIRST_NAME = ""
MY_LAST_NAME = ""
MY_SCHOOL = ""
MY_MAJOR = ""
COMPANY_NAME = ""
JOB_URL = ""
JOB_TITLE = ""
PAGE_LIMIT = 2

MESSAGE_TEMPLATE = """Hi {FirstName}!
My name is {MyFirstName} @ {MySchool} {MyMajor}.
I want to work at {CompanyName}.
Thanks!
"""

# ----------------------------------------------

def create_personalized_message(first_name):
    return MESSAGE_TEMPLATE.format(
        FirstName=first_name,
        MyFirstName=MY_FIRST_NAME,
        MyLastName=MY_LAST_NAME,
        MySchool=MY_SCHOOL,
        MyMajor=MY_MAJOR,
        CompanyName=COMPANY_NAME,
        JobUrl=JOB_URL,
        JobTitle=JOB_TITLE
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
    try:
        # Wait for the modal to appear
        modal = driver.find_element(By.CSS_SELECTOR, "div.artdeco-modal.send-invite")
        print(f"Result {idx}: Modal opened.")

        # Check for the "Add a note" button by aria-label
        try:
            add_note_button = modal.find_element(By.CSS_SELECTOR, "button[aria-label='Add a note']")
            add_note_button.click()
            print(f"Result {idx}: 'Add a note' button clicked.")
            time.sleep(0.5)

            # Find the textarea for the note
            textarea = modal.find_element(By.ID, "custom-message")
            textarea.clear()
            textarea.send_keys(personalized_message)
            print(f"Result {idx}: Added personalized message.")

            # Find and click the "Send" button
            send_button = modal.find_element(By.CSS_SELECTOR, "button.artdeco-button--primary")
            if send_button.is_enabled():
                send_button.click()
                print(f"Result {idx}: Invitation sent.")
            else:
                print(f"Result {idx}: 'Send' button is disabled.")
        except Exception:
            # If no "Add a note" button is present, fallback to sending without a note
            send_without_note_button = modal.find_element(By.CSS_SELECTOR, "button[aria-label='Send without a note']")
            send_without_note_button.click()
            print(f"Result {idx}: Sent invitation without a note.")

        time.sleep(0.2)

    except Exception as e:
        print(f"Result {idx}: Error while handling modal: {e}")

def send_invites_on_page(driver, search_url):
    driver.get(search_url)
    time.sleep(3)

    results = driver.find_elements(By.CSS_SELECTOR, "div.linked-area.flex-1.cursor-pointer")
    print(f"Found {len(results)} results on page: {search_url}")

    for idx, result in enumerate(results):
        try:
            # Access the first child of the main result container
            first_child = result.find_element(By.XPATH, "./div")
            children = first_child.find_elements(By.XPATH, "./div")

            if len(children) < 3:
                print(f"Skipping result {idx}: not enough child divs.")
                continue

            # Extract the button from the last child
            button = children[-1].find_element(By.TAG_NAME, "button")

            if "Connect" not in button.text:
                print(f"Result {idx}: Button does not contain 'Connect'. Skipping.")
                continue

            print(f"Result {idx}: Found button with text '{button.text}'.")

            # Scroll into view and click the button
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", button)
            button.click()
            print(f"Result {idx}: Clicked 'Connect' button.")
            time.sleep(0.5)

            # Extract the first name from the result
            first_name = result.find_element(By.CSS_SELECTOR, "a span[aria-hidden='true']").text.split(" ")[0]
            personalized_message = create_personalized_message(first_name)

            # Handle the modal
            handle_modal(driver, idx, personalized_message)

        except Exception as e:
            print(f"Result {idx}: Error while processing: {e}")


def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        login_to_linkedin(driver)
        print("Login completed!")

        for page in range(1, PAGE_LIMIT+1):
            page_url = BASE_SEARCH_URL + f"&page={page}"
            send_invites_on_page(driver, page_url)
            time.sleep(4)
            print(f"Page {page} finished!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
