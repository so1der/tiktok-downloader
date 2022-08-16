<h1>TikTok Video Downloader</h1>

So, this is basic TikTok video downloader, that downloads video from TikTok by using Selenium and requests libraries. Main problem in this case, is that TikTok website just wont give You direct URL to video, if You send simple get requests, despite that fact that this URL is locate in HTML code of page. Maybe thats because some .js scripts is responsible for creating HTML block that contains direct URL to video. But I have tried to render those scripts with python requests-html library, tried to send cookies (include s_v_webid), but it didn't work. So then I decided - why not come easier way. After all, why not use Selenium just to get this URL. After obtaining this URL, videocan be simply downloaded with requests library. So that how this downloader works - its open Your URL, find there direct video URL, and send get request to this direct video to download it. 

## Main advantage
The main advantage of this script is that it can download a bunch of TikToks, You just need to prepare .txt file, which contains links to videos.

Another advantage of this script, is that it does not depend on third party APIs or websites.

<img alt="automated download" align="center" src="https://raw.githubusercontent.com/so1der/tiktok-downloader/main/images/automated_download.png">

## Usage
To use this downloader, You need clone this repository 
```shell
git clone https://github.com/so1der/tiktok-downloader
cd tiktok-downloader
```
and install required libraries - Selenium, colorama, requests
```shell
pip install -r requirements.txt
```
You also need to download chromedriver, which matches Your browser version, from <a href="https://chromedriver.chromium.org/downloads">this website</a>, and put it in the same directory as .py files. So to work correctly, there should be at least 4 files in one directory: <i><b>main.py, headers.py, done.py</b></i> and <i><b>chromedriver.exe</b></i>. So after You intall all requirements, and download chromedriver - You are ready to go! Just execute main.py, and enter link, or path to .txt file. You also can just drop .txt file into Your console window, its will write path to file itself.

```shell
python main.py
```

## Executable file
If You dont have python installed, or if You dont want to install all of these requirements, You can just download .exe file at Releases. Unfortunately in this case You still need to download chromedriver. However, I have put chromedriver, that works with 103.0.5060.114 version of Chrome in archive.

## Supported link types
It supports all types of TikTok links

## Input format
Links in .txt file must be divided by newline.

If you just inserting links in console window, you must divide them by Spacebar.

## Browser
Yes, for now its works only with Google Chrome. But You can easily adapt it for other browser. You need to change these lines in file <i><b>main.py</i></b> to match Your browser's webdriver syntax:
```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
```
All these code lines are located in driverInit() function.

Due to prevalence of Google Chrome, I decided to make downloader work with it. But if dont use Chrome, and cant edit code, but still want to use this downloader - contact me, and I will help.

## Linux and video folder
I dont test this downloader on Linux, but I have a guess that You need to change 'PATH' in <b><i>config.ini</b></i> file, so downloader can work properly on Linux.

```ini
PATH = 'TikTokVideos\\'
```
As You can see, this variable contains path to folder in which videos will be downloaded. I suggest that in Linux this variable should be like this:
```ini
PATH = 'TikTokVideos/'
```
You can also change the folder name to Your liking.

## Speed and stability
Personally, I don't use tiktok, so thats why I wouldn't be able to fully test this downloader. But my friend did. He tested it with .txt file which contains 322 links to tiktok videos. You can see the results yourself. 322 videos downloaded in 15 minutes. Of course the speed also depends on Your internet connection, video length/quality, and PC specs, after all selenium operate a real browser. But despite this, it's still a good result I think.

<img alt="322 videos in 15 minutes" align="center" src="https://raw.githubusercontent.com/so1der/tiktok-downloader/main/images/result.png">

## Possible problems
- <i><b>Downloader output " ↑ was skipped, can't find video URL" error to all links</b></i>

This may be due to poor internet connection. The work of the downloader is arranged in such a way that it is waiting till certain "xgwrapper-4" block will appear. This block contains direct video URL, so if the block did not appear, the link may have led to the "Video currently unavailable" page. But if video is aviable, and downloader still output this error, You can increase "waiting" time, by changing TIME_OUT in <b><i>config.ini</b></i>
```ini
TIME_OUT = 10
# this will make downloader 'waiting' time equal to ten seconds
```

- <i><b>Downloader should work, but for some reason it still doesn't work</b></i>

A good way to debug problems is to comment out the line responsible for silently launching the browser:

```python
chrome_options.add_argument("--headless")
```

    ↓

```python
#chrome_options.add_argument("--headless")
```

This will allow You to see what happens on the webpage, and why downloader cant reach "xgwrapper-4" block for example.

- <i><b>Downloader crash and closes instantly, I can't see error message</b></i>

In this case You can execute downloader through terminal/cmd. Just enter:

```shell
python main.py
```
or
```shell
tiktok_downloader.exe
```
Or just drop .py/.exe file into console window. Even if it crush, it wont close cmd, this will allow You to see the error so You can fix it, or contact me.

# Changelog:
- 0.4:
Added debug mode.
Fixed problem when counter doesnt update in exception

- 0.3:
Reworked try-except block, so downloader wont break after exctept

# Conclusion

Despite that fact, that downloader already usable, it is still in the early stage of development. Thats why I will be very grateful for Your feedback. Together we can improve this downloader!
