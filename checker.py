import string
import threading
import time
import webbrowser
import os
import random

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

__directory = "./usernames_txt/"
unavailable_filename = "unavailable_usernames.txt"
taken_filename = "taken_usernames.txt"
available_filename = "available_usernames.txt"
all_user_filename = "all_usernames.txt"

os.makedirs(__directory, exist_ok=True)

with open(os.path.join(__directory, unavailable_filename), "w+") as file_usernames:
    file_usernames.close()
with open(os.path.join(__directory, available_filename), "w+") as file_usernames:
    file_usernames.close()
with open(os.path.join(__directory, taken_filename), "w+") as file_usernames:
    file_usernames.close()
with open(os.path.join(__directory, all_user_filename), "w+") as file_usernames:
    file_usernames.close()

with open("all_words.txt", "r", encoding="utf-8") as words_file:
    all_words = [word.strip() for word in words_file.readlines()]

file_mutex = threading.Lock()

# Получение абсолютного пути для файлов
unavailable_filepath = os.path.join(__directory, unavailable_filename)
taken_filepath = os.path.join(__directory, taken_filename)
available_filepath = os.path.join(__directory, available_filename)
all_user_filepath = os.path.join(__directory, all_user_filename)

def generate_readable_tag():
    while True:
        tag = random.choice(all_words)
        if not is_tag_in_file(tag, all_user_filepath):
            return tag

def write_to_file(tag, status):
    username = f"@{tag}"
    files = {
        "unavailable": unavailable_filepath,
        "taken": taken_filepath,
        "available": available_filepath,
    }

    filename = files.get(status, all_user_filepath)

    with file_mutex:
        if not os.path.exists(filename):
            with open(filename, "w+"):
                pass

        with open(filename, "a+") as file_usernames:
            file_usernames.write(f"{username}\n")
            print(f"[{status.upper()}] - {username} ")

def is_tag_in_file(tag, filename):
    with file_mutex:
        with open(filename, "r") as file_usernames:
            usernames = file_usernames.readlines()
            return tag in usernames


def parse_answer(tag):
    files = {
        "unavailable": "./usernames_txt/unavailable_usernames.txt",
        "taken": "./usernames_txt/taken_usernames.txt",
        "available": "./usernames_txt/available_usernames.txt",
    }

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
                    normalized_status = status_element.text.strip().lower()
                    filename = files.get(normalized_status, "all_usernames.txt")

                    if not is_tag_in_file(tag, filename):
                        write_to_file(tag, normalized_status)

                    break
            break
        finally:
            driver.quit()


def main():
    tag = generate_readable_tag()
    retries = 3

    for _ in range(retries):
        try:
            parse_answer(tag)
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)


if __name__ == '__main__':
    while True:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        s = Service(executable_path='./chromedriver.exe')
        driver = webdriver.Chrome(service=s, options=options)
        main()

