from get_chrome_version import get_chrome_version
from bs4 import BeautifulSoup
import requests
import difflib
import zipfile
import json
import wget
import os


def loadConfig():  
    return json.load(open('config.json'))

def getAllChomeVersion():
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
    return versions


def checkChromeVersion():
    chromeVersion = get_chrome_version()
    
    versionList = []
    for version in getAllChomeVersion():
        if version[0] not in versionList:
            versionList.append(version[0])

    return difflib.get_close_matches(chromeVersion, versionList)[0]


def downloadVersion(downloadVersion = checkChromeVersion()):
    fileLink = f'https://chromedriver.storage.googleapis.com/{downloadVersion}/chromedriver_win32.zip'
    wget.download(fileLink)

def extractZip():
    with zipfile.ZipFile('chromedriver_win32.zip', 'r') as zip_ref:
        zip_ref.extractall(loadConfig()['path'])

def deleteZip():
    for item in os.listdir(os.getcwd()):
        if item.endswith(".zip"):
            os.remove(os.path.join(os.getcwd(), item))

downloadVersion()
extractZip()
deleteZip()
loadConfig()


