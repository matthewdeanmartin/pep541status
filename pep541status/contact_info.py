from typing import List

import qypi.api as api
import requests
from qypi.__main__ import ENDPOINT

def get_users_info():
    que = api.QyPI(index_url=ENDPOINT)
    results = list(que.lookup_package(["termcolor"]))
    for data in results:
        for key, result in data["info"].items():
            if "author" in key or "_url" in key:
                if result and result != 'UNKNOWN':
                    print(key, result)

    # TODO: data mine for email addresses/websites
    for data in results:
        for name, releases in data["releases"].items():
            print(name)
            for file in releases:
                print(file["url"])

def get_all_maintainers_on_project(package:str):
    page = requests.get(f"https://pypi.org/project/{package}/")
    soup = BeautifulSoup(page.text, 'html.parser')
    links = []
    for link in soup.find_all("a"):
        url = link.attrs.get("href","")
        if "/user/" in url:
            links.append(url.replace("/user","").replace("/",""))
    return set(links)

from bs4 import BeautifulSoup
def get_all_packages(user:str)->List[str]:
    page = requests.get(f"https://pypi.org/user/{user}/")
    soup = BeautifulSoup(page.text, 'html.parser')
    links = []
    for link in soup.find_all("a"):
        url = link.attrs.get("href","")
        if "/project/" in url:
            links.append(url.replace("/project/","").replace("/",""))
    return set(links)

#
maintainers = get_all_maintainers_on_project("tinyrecord")
print(maintainers)
for maintainer in maintainers:
    print(get_all_packages(maintainer))