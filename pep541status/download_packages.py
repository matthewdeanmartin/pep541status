"""
Get some sample version strings from the wild.
"""
# https://python-forum.io/Thread-pip-list-available-packages

# download file
# curl!

# parse out version strings

# https://pypi.org/simple/epicurus/

import json

import os
import shutil
from os import listdir
from os.path import isfile, join

import requests

from pep541status.contact_info import get_all_maintainers_on_project, get_all_packages
from pep541status.utils.curl_commands import download_package
from pep541status.utils.email_utils import get_emails_in_text
from pep541status.utils.url_utils import get_urls_in_text


def package_info(rows):
    last = "nozips"
    for row in rows:
        try:
            url = row.split('"')[1]
            if ".zip" in url or ".gz" in url:
                print(url)
                last = url
        except:
            pass
    return last


def done_packages():
    packages = []
    for dir in os.listdir("packages"):
        if dir.endswith(".gz") or dir.endswith(".zip"):
            continue
        packages.append(dir)
    print("Have " + str(len(packages)) + " packages")
    return packages


def read_packages(rows):
    urls = []
    for row in rows:
        url = f"https://pypi.org/pypi/{row}/json"
        response = requests.get(url)
        meta = json.loads(response.text)
        # releases = [(key, value) for (key, value) in meta["releases"]]

        for version, info in meta["releases"].items():
            urls.extend([url["url"] for url in info])
    return urls



def get_packages_for(package):
    # read_packages(["qypi","jiggle-version","requests"])
    all_packages = []
    # Potentially any 1 collaborator could be the real contact
    for maintainer in get_all_maintainers_on_project(package):
        packages = get_all_packages(maintainer)
        all_packages.extend(packages)
    print(all_packages)
    return all_packages


def unpack_all(path: str):
    only_files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in only_files:
        target_directory = path + "/" + os.path.basename(file).replace(".tar.gz", "")
        if os.path.exists(target_directory):
            continue
        else:
            os.mkdir(target_directory)
        shutil.unpack_archive(path + "/" + file, target_directory)


from os import walk


def search_files_for_emails_websites(path):
    emails = []
    urls = []
    for (dirpath, dirnames, file_names) in walk(path):
        for file in file_names:
            print(file)
            if not file.endswith(".gz") and not file.endswith(".whl") and not file.endswith(".egg"):
                with open(dirpath + "/" + file, "r", encoding="utf-8", errors='ignore') as contents:
                    try:
                        text = contents.read()
                    except UnicodeError:
                        print("uh oh")
                        continue

                    emails_found = get_emails_in_text(text)
                    if emails_found:
                        print(file)
                    urls_found = get_urls_in_text(text)
                    if urls_found:
                        urls.append((str(file), tuple(set(urls_found))))
                    if emails_found:
                        emails.append((str(file), tuple(set(emails_found))))
    print(set(emails))
    print(set(urls))


def run():
    # dumps to current dir! ugh!
    all_packages = get_packages_for("jiggle-version")
    urls = read_packages(set(all_packages))
    download_package(urls, "../output/tmp5")

    unpack_all("../output/tmp5")
    search_files_for_emails_websites("../output/tmp5")

if __name__ == '__main__':
    run()