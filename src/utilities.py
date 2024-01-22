import os
import time
import json

from termcolor import colored
from datetime import datetime

def get_query(argv):
    """
    Checks if the user provided the search query through the arguments.
    """
    if "--query" in argv:
        query_index = argv.index("--query")
        query = argv[query_index + 1]

        return str(query)
    else:
        return None

def close_all_firefox_instances():
    """
    Closes all Firefox instances.
    """
    print(colored("[*] Closing all Firefox instances...", "yellow"))

    if os.name == "nt":
        os.system("taskkill /im firefox.exe /f")
    elif os.name == "posix":
        os.system("killall firefox")
    else:
        print(colored("[!] Unsupported OS.", "red"))
        exit(1)

def get_people_list_from_file(argv):
    """
    Checks if the user has specified a file containing a list of people using the --people flag.
    If yes, returns the list of people. If no, ask for it.
    """
    if "--people" in argv:
        people_index = argv.index("--people")
        people_file = argv[people_index + 1]

        # Check if file exists
        if not os.path.exists(people_file):
            print(colored("[!] File not found.", "red"))
            exit(1)

        # Check if file is a file
        if not os.path.isfile(people_file):
            print(colored("[!] Not a file.", "red"))
            exit(1)

        # Read file
        return json.loads(open(people_file, "r").read())

def scroll_to_bottom(driver):
    """
    Scrolls to the bottom of the page.
    """
    print(colored("[*] Scrolling to bottom of page...", "yellow"))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def print_ascii_art():
    """
    Prints out the ASCII Art logo.
    """
    with open("assets/ascii_art.txt", "r") as f:
        ascii_art = f.read()
        print(colored(ascii_art, "cyan"))

def get_n_search_results(argv):
    """
    Checks if the user has specified the number of search results to scrape using the --n flag.
    If yes, returns the number of search results. If no, ask for it.
    """
    if "--n" in argv:
        n_index = argv.index("--n")
        n = argv[n_index + 1]
        return int(n)
    else:
        print(colored("[*] Using default amount of search results: 30", "magenta"))
        return None

def start_message():
    """
    Prints out the starting message.
    """
    print(colored("[*] Initializing browser...", "yellow"))

def get_firefox_profile_location(argv):
    """"
    Checks if the user has specified a Firefox profile location using the --profile flag.
    If yes, returns the location of the profile. If no, ask for it.
    """
    if "--profile" in argv:
        profile_index = argv.index("--profile")
        profile_location = argv[profile_index + 1]
        return profile_location
    else:
        return input(colored("[?] Enter the location of your Firefox profile: ", "magenta"))

def get_headless(argv):
    """
    Checks if the user has specified the --headless flag.
    If yes, returns True. If no, returns False.
    """
    if "--headless" in argv:
        return True
    else:
        return False
    
def check_profile_location(path):
    """
    Checks if the specified path is a directory.
    """
    # Check if Firefox profile exists
    if not os.path.exists(path):
        print(colored("[!] Firefox profile not found.", "red"))
        exit(1)

    # Check if Firefox profile is a directory
    if not os.path.isdir(path):
        print(colored("[!] Firefox profile is not a directory.", "red"))
        exit(1)

def wait(s):
    """
    Waits for s seconds.
    """
    time.sleep(s)

def prepare_strucutre():
    """
    Prepares the output directory and the output file.
    """
    # Create output directory
    if not os.path.exists("output"):
        os.mkdir("output")


def save_to_json(data):
    """
    Saves the data to a JSON file.
    """
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"output/{timestamp}.json"

    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=4))

    print(colored(f"[+] Saved data to {filename}", "green"))
