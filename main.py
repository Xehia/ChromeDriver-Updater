import requests
import difflib
import wget
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

    for version in versions:
        if version[0] == downloadVersion:
            downloadLink = version[1]

    req = requests.get(downloadLink)
    soup = BeautifulSoup(req.content, 'html.parser')

    for a in soup.find_all('a', href=True):
        if a['href'].endswith('win32.zip'):
                wget.download(downloadLink)
                print(downloadLink)
                print("Downloaded version: "+ downloadVersion)

downloadVersion()


