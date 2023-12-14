import random
import string
import threading
import time
import webbrowser

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# options = webdriver.ChromeOptions()
# options.add_argument('headless')"
s = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=s)


#   Р А Н Д О М     Н И К И

def generate_readable_tag(min_length=6, max_length=8):
    consonants = 'bcdfghjklmnpqrstvwxyz'
    vowels = 'aeiou'

    while True:
        length = random.randint(min_length, max_length)
        tag = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))
        tag += ''.join([random.choice(consonants) if i % 2 == 0 else random.choice(vowels) for i in range(length - 1)])
        tag = tag[:11]

        if is_tag_in_file(tag):
            return tag


file_mutex = threading.Lock()


def write_to_file(tag, status):
    username = f"@{tag}"
    file_mapping = {
        "unavail": "unavail_usernames.txt",
        "taken": "taken_usernames.txt",
        "avail": "avail_usernames.txt",
    }

    filename = file_mapping.get(status, "default_usernames.txt")

    with file_mutex:
        with open(filename, "a+") as file_usernames:
            file_usernames.write(f"{username}\n")


def is_tag_in_file(tag):
    if tag:
        return tag
    else:
        pass


def parse_answer(tag):
    retries = 3
    for _ in range(retries):
        try:
            driver.get(f'https://fragment.com/?query={tag}')
            time.sleep(5)
            bs = BeautifulSoup(driver.page_source, "html.parser")
            block = bs.find("tbody", class_="tm-high-cells")

            for status in ["unavail", "taken", "avail"]:
                status_element = block.find("div", class_=f"table-cell-value tm-value tm-status-{status}")
                if status_element:
                    if status_element.text.strip().lower() == status:
                        write_to_file(tag, status)
                    break

            break
        except Exception as e:
            time.sleep(10)
            pass


def main():
    tag = generate_readable_tag()
    parse_answer(tag)


if __name__ == '__main__':
    while True:
        main()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        s = Service(executable_path='./chromedriver.exe')
        driver = webdriver.Chrome(service=s, options=options)
