import os.path
import time
import re
import os

from colorama import init
import selenium
import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

from done import grandFinale
from headers import headers


PATH = 'TikTokVideos\\'
TIME_OUT = 6

def directoryCreator():
    try:
        os.mkdir(PATH)
        print("TikTokVideos directory was created successfully, "
              "videos will be downloaded in it\n")
    except FileExistsError:
        print("TikTokVideos directory already exists, "
              "videos will be downloaded in it\n")


def downloadTikToks(urls, n=1):
    amount = len(urls)
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches',
                                           ['enable-logging'])
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--output=/dev/null")
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except selenium.common.exceptions.SessionNotCreatedException:
        input("Session not created. Check version of your webdriver/browser\n")
        exit()
    except selenium.common.exceptions.WebDriverException:
        input("Webdriver not found in current directory.\n")
        exit()

    global_time = time.time()
    try:
        for url in urls:
            print(f'\033[36m Downloading ({n}/{amount}): \033[39m')
            url = url.strip()
            print(url)

            if url.find('tiktok') == -1:
                print('\033[31m ↑ was skipped, Incorrect TikTok URL\033[39m\n')
                n += 1
                continue

            url_type_checker = url.split('https://')

            if url_type_checker[1].startswith('vm'):
                file_name = (url.split("/"))[3]
            else:
                file_name = re.search('\d{19}', url).group(0)

            if os.path.isfile(f'{PATH}{file_name}.mp4'):
                print('\033[35m ↑ was skipped, Already downloaded \033[39m\n')
                n += 1
                continue
            start_time = time.time()
            driver.get(url)
            wait = WebDriverWait(driver, TIME_OUT)
            video_id = re.search('\d{19}', driver.current_url).group(0)
            try:
                video_url = wait.until(EC.presence_of_element_located(
                                      (By.ID, f'xgwrapper-4-{video_id}')))
            except:
                print("\033[31m ↑ was skipped, can't find video URL\033[39m\n")
                n += 1
                continue
            wrapper = driver.find_element(By.ID, f'xgwrapper-4-{video_id}')
            video_tag = wrapper.find_element(By.TAG_NAME, "video")
            video_link = video_tag.get_attribute('src')
            video = requests.get(video_link, headers=headers)
            with open(f'{PATH}{file_name}.mp4', 'wb') as f:
                f.write(video.content)
            print('\033[32m ↑ was downloaded successfully\033[39m')
            print("--- %s seconds ---\n" % (time.time() - start_time))
            n += 1
    except Exception as e:
        print(f"\033[31m Unexpected {e=}, {type(e)=}")
        driver.close()
        input()
        exit()
    finally:
        driver.close()
        minutes = int((time.time() - global_time) // 60)
        seconds = int((time.time() - global_time) % 60)
        print('\033[36m Total time spent:'
              f'\033[39m {minutes} minutes and {seconds} seconds')


def urlsListHandler():
    prompt = input('Drop .txt file here or insert links, and press Enter:\n')
    while True:
        try:
            if prompt.startswith('https://'):
                urls = prompt.split(' ')
                break
            with open(prompt, 'r') as f:
                urls = f.readlines()
            break
        except FileNotFoundError:
            prompt = input('Incorrect file or link. Try again:\n')
    return urls

if __name__ == '__main__':
    init()
    directoryCreator()
    urls = urlsListHandler()
    downloadTikToks(urls)
    grandFinale()
    input()
