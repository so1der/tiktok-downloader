import os.path
import time
import re
import os
import configparser

from colorama import Fore, init
import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

from done import grand_finale
from headers import headers


class TikTokDownloader:
    def __init__(self):
        self.count = 1
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.PATH = config.get('CONFIG', 'PATH', fallback='TikTokVideos\\')
        self.TIME_OUT = int(config.get('CONFIG', 'TIME_OUT', fallback=6))
        self.DEBUG_MODE = config.get('CONFIG', 'DEBUG_MODE', fallback='False')

    def init_driver(self):
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches',
                                               ['enable-logging'])
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)

    def create_directory(self):
        if os.path.exists(self.PATH):
            return print(f"{self.PATH} directory already exists")
        os.mkdir(self.PATH)
        print(f"{self.PATH} directory was created successfully")

    def get_list(self):
        prompt = input('Drop txt file here or insert links and press Enter:\n')
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

    def create_log(self, links):
        date = (time.asctime(time.localtime()))
        date = date.replace(' ', '_').replace(':', '-')
        with open(f'undownoaded {date}.txt', 'w') as f:
            for link in links:
                f.write(f'{link}\n')

    def isnt_tiktok(self, url):
        if url.find('tiktok') == -1:
            print(Fore.RED + ' ↑ Incorrect TikTok URL\n')
            self.count += 1
            return True

    def already_downloaded(self,  video_id):
        if os.path.isfile(f'{self.PATH}{video_id}.mp4'):
            print(f'{Fore.MAGENTA} ↑ Already downloaded\n')
            self.count += 1
            return True

    def get_video_link(self, video_id):
        wrapper = self.driver.find_element(By.ID, f'xgwrapper-4-{video_id}')
        video_tag = wrapper.find_element(By.TAG_NAME, "video")
        video_link = video_tag.get_attribute('src')
        return video_link

    def download_video(self, video_link, video_id):
        video = requests.get(video_link, headers=headers)
        with open(f'{self.PATH}{video_id}.mp4', 'wb') as f:
            f.write(video.content)
        print(f'{Fore.GREEN} ↑ was downloaded successfully')

    def calculate_total_time(self, global_time):
        minutes = int((time.time() - global_time) // 60)
        seconds = int((time.time() - global_time) % 60)
        return minutes, seconds

    def download(self, urls):
        amount = len(urls)
        global_time = time.time()
        self.driver = self.init_driver()
        undownloaded = []
        for url in urls:
            try:
                print(f'{Fore.CYAN} Downloading ({self.count}/{amount}):')
                url = url.strip()
                print(url)
                if self.isnt_tiktok(url):
                    continue
                start_time = time.time()
                self.driver.get(url)
                wait = WebDriverWait(self.driver, self.TIME_OUT)
                video_id = re.search('\d{19}', self.driver.current_url).group()
                if self.already_downloaded(video_id):
                    continue
                try:
                    wait.until(EC.presence_of_element_located(
                            (By.ID, f'xgwrapper-4-{video_id}')))
                except:
                    print(f"{Fore.RED} ↑ can't find video URL\n")
                    undownloaded.append(url)
                    self.count += 1
                    continue
                video_link = self.get_video_link(video_id)
                self.download_video(video_link, video_id)
                print(f"--- {time.time() - start_time} seconds ---\n")
                self.count += 1
            except Exception as e:
                if self.DEBUG_MODE == 'True':
                    print(f"{Fore.RED} Unexpected {e}, {type(e)}")
                else:
                    print(f'{Fore.RED} ↑ was skipped, error {e.args[0]}\n')
                undownloaded.append(url)
                self.count += 1
        self.create_log(undownloaded)
        minutes, seconds = self.calculate_total_time(global_time)
        print(Fore.CYAN + ' Total time spent: '
              f'{Fore.WHITE}{minutes} minutes and {seconds} seconds')

    def terminate_driver(self):
        self.driver.quit()

    def start(self):
        self.create_directory()
        self.download(self.get_list())
        self.terminate_driver()

if __name__ == '__main__':
    init(autoreset=True)
    tiktokdownloader = TikTokDownloader()
    tiktokdownloader.start()
    grand_finale()
    input()
