import os
import subprocess
import winreg
from utilities import * 
from motherboard import *

# Define the URL to download Dell SupportAssist
support_assist_download_url = "https://downloads.dell.com/serviceability/catalog/SupportAssistInstaller.exe"

# Set the installer path to the specified download folder
user_download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
dell_support_assist_installer_filename = "SupportAssistInstaller.exe"
support_assist_installer_path = os.path.join(user_download_folder, dell_support_assist_installer_filename)

def launch_dell_support_assist():
    try:
        ps_command = (
            "Get-AppxPackage | Where-Object {$_.Name -like '*SupportAssist*'} | "
            "Foreach-Object {"
            "$packageName = $_.PackageFamilyName;"
            "Start-Process shell:AppsFolder\\$packageName!App;"
            "}"
        )
        subprocess.run(["powershell", "-Command", ps_command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching the UWP app: {e}")

def install_support_assist():
    download_installer(url=support_assist_download_url, user_download_folder=user_download_folder,installer_path=support_assist_installer_path)
    # Install Dell SupportAssist
    install_program(support_assist_installer_path, "Dell Support Assist")

# Check if Dell SupportAssist is already installed
def check_and_launch_dell_support_assist():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Dell\SupportAssistAgent", 0, winreg.KEY_READ):
            launch_dell_support_assist()
    except FileNotFoundError:
        install_support_assist()

def dell():
    print(mobo_manufacturer())
    check_and_launch_dell_support_assist()