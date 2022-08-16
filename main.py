from distutils.debug import DEBUG
import os.path
import time
import re
import os
import configparser

from colorama import Fore, init
import selenium
import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

from done import grandFinale
from headers import headers

# Reading constants form .ini file
config = configparser.ConfigParser()
config.read('config.ini')
PATH = config.get('CONFIG', 'PATH', fallback='TikTokVideos\\')
TIME_OUT = int(config.get('CONFIG', 'TIME_OUT', fallback=6))
DEBUG_MODE = config.get('CONFIG', 'DEBUG_MODE', fallback='False')


def directoryCreator():
    if os.path.exists(PATH):
        return print(f"{PATH} directory already exists, "
                      "videos will be downloaded in it\n")
    os.mkdir(PATH)
    print(f"{PATH} directory was created successfully, "
           "videos will be downloaded in it\n")


def urlsListHandler():
    prompt = input('Drop .txt file here or insert links, and press Enter:\n')
    while True:
        if prompt.startswith('https://'):
            urls = prompt.split(' ')
            break
        try:
            with open(prompt, 'r') as f:
                urls = f.readlines()
            break
        except FileNotFoundError:
            prompt = input('Incorrect file or link. Try again:\n')
    return urls


def driverInit():
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches',
                                           ['enable-logging'])
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)


def undownloadedLinksLogFile(links):
    date = (time.asctime(time.localtime())).replace(' ', '_').replace(':', '_')
    with open(f'undownoaded {date}.txt', 'a') as f:
        for link in links:
            f.write(f'{link}\n')


def downloadTikToks(urls, n=1):
    amount = len(urls)
    try:
        driver = driverInit()
    except selenium.common.exceptions.SessionNotCreatedException:
        input("Session not created. Check version of your webdriver/browser\n")
        exit()
    except selenium.common.exceptions.WebDriverException:
        input("Webdriver not found in current directory.\n")
        exit()
    global_time = time.time()
    undownloaded_links = []
    for url in urls:
        try:
            print(f'{Fore.CYAN} Downloading ({n}/{amount}):')
            url = url.strip()
            print(url)
            if url.find('tiktok') == -1:
                print(Fore.RED + ' ↑ was skipped, Incorrect TikTok URL\n')
                n += 1
                continue
            start_time = time.time()
            driver.get(url)
            wait = WebDriverWait(driver, TIME_OUT)
            video_id = re.search('\d{19}', driver.current_url).group(0)
            if os.path.isfile(f'{PATH}{video_id}.mp4'):
                print(Fore.MAGENTA + ' ↑ was skipped, Already downloaded\n')
                n += 1
                continue
            try:
                wait.until(EC.presence_of_element_located(
                          (By.ID, f'xgwrapper-4-{video_id}')))
            except:
                print(Fore.RED + " ↑ was skipped, can't find video URL\n")
                undownloaded_links.append(url)
                n += 1
                continue
            wrapper = driver.find_element(By.ID, f'xgwrapper-4-{video_id}')
            video_tag = wrapper.find_element(By.TAG_NAME, "video")
            video_link = video_tag.get_attribute('src')
            video = requests.get(video_link, headers=headers)
            with open(f'{PATH}{video_id}.mp4', 'wb') as f:
                f.write(video.content)
            print(Fore.GREEN + ' ↑ was downloaded successfully')
            print(f"--- {time.time() - start_time} seconds ---\n")
            n += 1
        except Exception as e:
            if DEBUG_MODE == 'True':
                print(f"{Fore.RED} Unexpected {e}, {type(e)}")
            else:
                print(f'{Fore.RED} ↑ was skipped, error {e.args[0]}\n')
            undownloaded_links.append(url)
            n += 1
    driver.close()
    undownloadedLinksLogFile(undownloaded_links)
    minutes = int((time.time() - global_time) // 60)
    seconds = int((time.time() - global_time) % 60)
    print(Fore.CYAN + ' Total time spent: '
          f'{Fore.WHITE}{minutes} minutes and {seconds} seconds')

if __name__ == '__main__':
    init(autoreset=True)
    directoryCreator()
    urls = urlsListHandler()
    downloadTikToks(urls)
    grandFinale()
    input()
