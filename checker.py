import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import webbrowser
import random
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('headless')
s = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)


# def generate_readable_tag(min_length=5, max_length=5):
#     consonants = 'bcdfghjklmnpqrstvwxyz'
#     vowels = 'aeiou'
#
#     while True:
#         length = random.randint(min_length, max_length)
#         tag = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))
#         tag += ''.join([random.choice(consonants) if i % 2 == 0 else random.choice(vowels) for i in range(length - 1)])
#         tag = tag[:11]
#
#         if not is_tag_in_file(tag, 'list_usernames.txt'):
#             return tag





def is_tag_in_file(tag, filename):
    with open(filename, 'r') as file:
        usernames = file.read().splitlines()
        return tag in usernames


def parse_answer(tag):
    driver.get(f'https://fragment.com/?query={tag}')
    #    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tm-high-cells")))
    time.sleep(5)

    bs = BeautifulSoup(driver.page_source, "html.parser")
    block = bs.find("tbody", class_="tm-high-cells")

    try:
        if block.find("div", class_=f"table-cell-value tm-value tm-status-unavail"):
            unavail_username = f"@{tag}"
            print(unavail_username)
            with open("unavail_usernames.txt", "a+") as file_usernames:
                file_usernames.write(f"{unavail_username}\n")
                file_usernames.close()

        elif block.find("div", class_=f"table-cell-value tm-value tm-status-taken"):
            taken_username = f"@{tag}"
            with open("taken_usernames.txt", "a+") as file_usernames:
                file_usernames.write(f"{taken_username}\n")
                file_usernames.close()

        else:
            avail_username = f"@{tag}"
            with open("avail_usernames.txt", "a+") as file_usernames:
                file_usernames.write(f"{avail_username}\n")
                file_usernames.close()

    except Exception as e:
        print(e)
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
