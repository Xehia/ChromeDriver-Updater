import requests
import difflib
import zipfile
import wget
import os
from get_chrome_version import get_chrome_version
from bs4 import BeautifulSoup

url = "https://chromedriver.chromium.org/downloads"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

versions = []

for a in soup.find_all('a', href=True):
    if a['href'].startswith('https://chromedriver.storage.googleapis'):
        if a['href'].endswith('notes.txt'):
            pass
        else:
            version = (a['href'].split('?')[1].split('=')[1])[:-1]

            currentDict = [version, a['href']]
            versions.append(currentDict)


def checkChromeVersion():
    chromeVersion = get_chrome_version()
    
    versionList = []
    for version in versions:
        if version[0] not in versionList:
            versionList.append(version[0])

    return difflib.get_close_matches(chromeVersion, versionList)[0]


def downloadVersion(downloadVersion = checkChromeVersion()):
    fileLink = f'https://chromedriver.storage.googleapis.com/{downloadVersion}/chromedriver_win32.zip'
    wget.download(fileLink)

def extractZip():
    with zipfile.ZipFile('chromedriver_win32.zip', 'r') as zip_ref:
        zip_ref.extractall('')

downloadVersion()
extractZip()

app_path = os.path.join(os.getcwd())
os.environ["path"] += app_path


