import sys

from utilities import *
from selenium_firefox import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Enter your search query or keywords here
SEARCH_QUERY = "Restaurant owner"

# Enter the GEO_URN of your location
# you can find it by searching for your location on LinkedIn
GEO_URN = "[\"103644278\"]" # Current location is `United States`

# This determines whether the script will ask you before sending the connection request
# to someone, or not.
ASK_BEFORE_SENDING = False

# How many people you want to connect to
N_SEARCH_RESULTS = 100

# The message you want to send to the people
# The only variable right now is {{name}}, which will be replaced by the person's name
MESSAGE_WITH_NAME = "Hello {{name}}, I would love to connect with you! I hope you are having a great day."
MESSAGE_WITHOUT_NAME = "Hello, I would love to connect with you! I hope you are having a great day."

# From which page to start getting people
CURRENT_PAGE = 1

# IMPORTANT
# Change this depending on your language
CONTENT_OF_ADD_MESSAGE_BUTTON = "Nachricht hinzufügen"
CONTENT_OF_SEND_BUTTON = "Senden"
CONTENT_OF_MORE_BUTTON = "Mehr"
CONTENT_OF_CONNECTION_BUTTON = "Vernetzen"

# ---- DON'T TOUCH ----
PEOPLE = []
MAX_PAGES = 10
BASE_LINKEDIN_URL = "https://www.linkedin.com"
RESULTS_LIST_CLASS = "reusable-search__entity-result-list"
PAGINATION_LIST_CLASS = "artdeco-pagination__pages"
PERSON_NAME_CLASS = "entity-result__title-text"
PERSON_SUBTITLE_CLASS = "entity-result__primary-subtitle"
PERSON_SECONDARY_SUBTITLE_CLASS = "entity-result__secondary-subtitle"
PERSON_SUMMARY_CLASS = "entity-result__summary"
PERSON_ACTION_BUTTON = "entity-result__actions"
ACTION_CONTAINER = "IZLqPHsLPvmtnxTRikvwkBUVdnExLjJlPwssjbtQ" # Untested, might not work. Open an issue if it does not.
MODAL_ACTION_BAR = "artdeco-modal__actionbar"

def main():
    """
    Main function, where all the magic happens.
    """
    global PEOPLE
    global MAX_PAGES
    global SEARCH_QUERY
    global CURRENT_PAGE
    global N_SEARCH_RESULTS

    # Print Art
    print_ascii_art()

    if "--help" in sys.argv:
        print(colored("[*] Help:", "magenta"))
        print(colored("    --n <number> - Specify the number of search results to scrape.", "magenta"))
        print(colored("    --profile <location> - Specify the location of your Firefox profile.", "magenta"))
        print(colored("    --headless - Specify if you want to run the script headless or not.", "magenta"))
        print(colored("    --query <query> - Specify the query you want to search for.", "magenta"))
        print(colored("    --people <file> - Specify the file you want to load people from.", "magenta"))
        print(colored("    --help - Show this help message.\n\n", "magenta"))
        return

    # Close all Firefox instances
    close_all_firefox_instances()

    # Starting Message
    start_message()

    # Prepare folder structure
    prepare_strucutre()

    # Check if user supplied --n flag
    temp_n_search_results = get_n_search_results(sys.argv)

    if temp_n_search_results:
        N_SEARCH_RESULTS = temp_n_search_results

    # Load people from file
    temp_people = get_people_list_from_file(sys.argv)

    if temp_people:
        print(colored(f"[+] Loaded {len(temp_people)} people from file.", "green"))
        PEOPLE = temp_people

    # See if user supplied a custom query
    temp_query = get_query(sys.argv)

    if temp_query:
        SEARCH_QUERY = temp_query

    # Get Firefox Profile Location and check if it is valid
    firefox_profile_location = get_firefox_profile_location(sys.argv)
    check_profile_location(firefox_profile_location)

    # Get headless option
    headless = get_headless(sys.argv)

    # Instantiate Firefox Options
    options = Options()

    if headless:
        options.add_argument("--headless")

    # Bypass the bug in Selenium using this method
    # More Information: https://github.com/SeleniumHQ/selenium/issues/11028
    options.add_argument("-profile")
    options.add_argument(firefox_profile_location)

    # Instantiate Firefox Service
    service = Service(GeckoDriverManager().install())

    # Instantiate Firefox Driver
    driver = webdriver.Firefox(service=service, options=options)

    if not temp_people:
        # Go to LinkedIn
        driver.get(f"{BASE_LINKEDIN_URL}/search/results/people/?geoUrn={GEO_URN}&keywords={SEARCH_QUERY}&origin=SWITCH_SEARCH_VERTICAL&sid=p%2CR")

        # Set full screen
        driver.maximize_window()

        # Wait for page load
        wait(4)

        # Scroll to bottom of page
        scroll_to_bottom(driver)

        wait(2)

        # Get pagination list
        pagination_list = driver.find_element(By.CLASS_NAME, PAGINATION_LIST_CLASS)

        # Get last `li` element's text (inside of `span`)
        last_page_number = int(pagination_list.find_elements(By.TAG_NAME, "li")[-1].find_element(By.TAG_NAME, "span").text)
        MAX_PAGES = last_page_number
        for _ in range(MAX_PAGES):
            if len(PEOPLE) >= N_SEARCH_RESULTS:
                break

            # Print current page message
            print(colored(f"[+] Navigating to page {CURRENT_PAGE}...", "yellow"))

            # Go to Page URL
            driver.get(f"{BASE_LINKEDIN_URL}/search/results/people/?geoUrn={GEO_URN}&keywords={SEARCH_QUERY}&origin=SWITCH_SEARCH_VERTICAL&sid=p%2CR&page={CURRENT_PAGE}")

            # Get results list
            results_list = driver.find_element(By.CLASS_NAME, RESULTS_LIST_CLASS)

            # Get all `li` elements inside of the results list
            results = results_list.find_elements(By.TAG_NAME, "li")

            # Iterate over results, get their information
            for result in results:

                # Get PFP URL
                try:
                    pfp = result.find_element(By.TAG_NAME, "img").get_attribute("src")
                except:
                    pfp = ""

                # Get Profile URL
                try:
                    profile_url = result.find_elements(By.TAG_NAME, "a")
                    for url in profile_url:
                        if "/in/" in url.get_attribute("href"):
                            profile_url = url.get_attribute("href")
                            break
                    else:
                        profile_url = ""
                except:
                    profile_url = ""

                # Get Name
                try:
                    name = result.find_element(By.CLASS_NAME, PERSON_NAME_CLASS).find_elements(By.TAG_NAME, "span")[1].text
                except:
                    continue

                # Get Subtitle
                try:
                    subtitle = result.find_element(By.CLASS_NAME, PERSON_SUBTITLE_CLASS).text
                except:
                    subtitle = ""

                # Get Secondary Subtitle
                try:
                    secondary_subtitle = result.find_element(By.CLASS_NAME, PERSON_SECONDARY_SUBTITLE_CLASS).text
                except:
                    secondary_subtitle = ""

                # Get Summary
                try:
                    summary = result.find_element(By.CLASS_NAME, PERSON_SUMMARY_CLASS).text
                except:
                    summary = ""


                PEOPLE.append({
                    "pfp": pfp,
                    "name": name,
                    "profile_url": profile_url,
                    "subtitle": subtitle,
                    "secondary_subtitle": secondary_subtitle,
                    "summary": summary
                })

            # Increment current page
            CURRENT_PAGE += 1

        # Remove every person without profile_url
        PEOPLE = [person for person in PEOPLE if person["profile_url"]]

        # Save to JSON
        save_to_json(PEOPLE)

    # Tell user how many people were found
    print(colored(f"[+] Found {len(PEOPLE)} people.", "green"))

    input(colored("[?] Press any key to start sending connection requests...", "magenta"))

    # ----------------------------------------------------------- #
    # This is where the script begins sending connection requests #
    # ----------------------------------------------------------- #

    for person in PEOPLE:
        print(colored(f"[+] Sending connection request to {person['name'] if person['name'] else person['subtitle']}...", "yellow"))

        # Navigate to profile url
        driver.get(person["profile_url"])

        # Wait for page load
        wait(2)

        # Get action container
        action_container = driver.find_element(By.CLASS_NAME, ACTION_CONTAINER)

        # Get all buttons
        buttons = action_container.find_elements(By.TAG_NAME, "button")

        # Iterate over buttons
        for button in buttons:
            # Check if button contains the text "Vernetzen"
            try:
                if CONTENT_OF_CONNECTION_BUTTON in button.find_element(By.TAG_NAME, "span").text:
                    # Click the button
                    button.click()
                    break
            except:
                continue
        else:
            # WARNING: This does not work yet
            print(colored("[!] Could not find the connection button the conventional way.", "red"))

            """
            try:
                # Get all buttons
                buttons = action_container.find_elements(By.TAG_NAME, "button")

                # Iterate over buttons
                for button in buttons:
                    # Check if button contains the text "Mehr"
                    try:
                        if CONTENT_OF_MORE_BUTTON in button.find_element(By.TAG_NAME, "span").text:
                            # Click the button
                            button.click()
                            break
                    except:
                        continue

                # artdeco-dropdown__content-inner
                dropdown = driver.find_element(By.CLASS_NAME, "artdeco-dropdown__content-inner").find_element(By.TAG_NAME, "ul")

                # Get all `span` elements
                dropdown_items = dropdown.find_elements(By.TAG_NAME, "span")

                for item in dropdown_items:
                    if CONTENT_OF_CONNECTION_BUTTON in item.text:
                        # Get parent `div` element
                        parent = item.find_element(By.XPATH, "..")

                        # Click the parent element
                        parent.click()

                        break
            except:
                continue
            """
        try:
            # Get modal action bar
            modal_action_bar = driver.find_element(By.CLASS_NAME, MODAL_ACTION_BAR)

            # Get all buttons
            buttons = modal_action_bar.find_elements(By.TAG_NAME, "button")

            # Iterate over buttons
            for button in buttons:
                # Check if button contains the text "Nachricht hinzufügen"
                try:
                    if CONTENT_OF_ADD_MESSAGE_BUTTON in button.find_element(By.TAG_NAME, "span").text:
                        # Click the button
                        button.click()
                        break
                except:
                    continue
            else:
                print(colored("[!] Could not find the add message button.", "red"))
                continue

            # Find custom message textarea, by ID
            custom_message_textarea = driver.find_element(By.ID, "custom-message")

            # Clear the textarea
            custom_message_textarea.clear()

            # Check if the person has a name
            if person["name"]:
                # Send message with name
                custom_message_textarea.send_keys(MESSAGE_WITH_NAME.replace("{{name}}", person["name"]))
            else:
                # Send message without name
                custom_message_textarea.send_keys(MESSAGE_WITHOUT_NAME)

            # Get all buttons
            buttons = modal_action_bar.find_elements(By.TAG_NAME, "button")

            # Iterate over buttons
            for button in buttons:
                # Check if button contains the text "Senden"
                try:
                    if CONTENT_OF_SEND_BUTTON in button.find_element(By.TAG_NAME, "span").text:
                        # Click the button
                        if ASK_BEFORE_SENDING:
                            input(colored("[?] Press any key to send the connection request...", "magenta"))
                        button.click()
                        wait(0.7)
                        print(colored(f"[+] Sent {person['name']} a connection request.", "green"))
                        break
                except:
                    continue
            else:
                print(colored("[!] Could not find the send button.", "red"))
                continue
        except Exception as err:
            print(colored(f"[*] Error: {err}", "red"))
            continue

    print(colored("\n[+] Done.", "green"))


if __name__ == "__main__":
    main()
