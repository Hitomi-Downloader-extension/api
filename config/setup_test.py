import requests
import zipfile
import os
import shutil


print("Get release info from Github")
github_api_response = requests.get(
    "https://api.github.com/repos/KurtBestor/Hitomi-Downloader/releases"
)

print("Get latest release info")
downloader_install_url = github_api_response.json()[0]["assets"][0][
    "browser_download_url"
]

print("Download latest release")
downloader_zip_response = requests.get(downloader_install_url)

print("Save latest release")
with open("Hitomi-Downloader.zip", "wb") as f:
    f.write(downloader_zip_response.content)

print("Extract latest release")
with zipfile.ZipFile("Hitomi-Downloader.zip", "r") as zip_ref:
    zip_ref.extractall(".")

print("Delete zip file")
os.remove("Hitomi-Downloader.zip")

print("Make scripts folder for test")
os.mkdir("scripts")

print("Copy scripts")
shutil.copyfile("api.py", "scripts/api.py")
print("Copy config")
shutil.copyfile("config/hitomi_downloader_GUI.ini", "hitomi_downloader_GUI.ini")

print("Done")
