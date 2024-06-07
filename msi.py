import os
import subprocess
import winreg
import zipfile
from utilities import *
import glob
# Define the URL to download MSI Center
msi_center_download_url = "https://download.msi.com/uti_exe/desktop/MSI-Center.zip"

# Set the installer path to the specified download folder
user_download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
msi_center_installer_path = glob.glob(os.path.join(user_download_folder, 'MSI Center*.exe'))

def is_msi_center_installed():
    cmd = 'powershell "Get-AppxPackage -AllUsers | Where-Object {$_.Name -like \'*MSICenter*\' -or $_.Name -like \'*MSIcenter*\' -or $_.Name -like \'*MSI center*\'}"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return 'MSICenter' in result.stdout or 'MSIcenter' in result.stdout or 'MSI center' in result.stdout

def launch_msi_center():
    try:
        ps_command = (
            "Get-AppxPackage | Where-Object {$_.Name -like '*MSI Center*'} | "
            "Foreach-Object {"
            "$packageName = $_.PackageFamilyName;"
            "Start-Process shell:AppsFolder\\$packageName!App;"
            "}"
        )
        subprocess.run(["powershell", "-Command", ps_command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching the UWP app: {e}")


def unzip(file_name_to_unzip, unzip_destination):
    with zipfile.ZipFile(file_name_to_unzip, 'r') as zip_ref:
    # Perform operations on the ZIP file
        zip_ref.extractall(unzip_destination)
        zip_ref.close()

def install_msi_center():
    download_installer(url=msi_center_download_url, user_download_folder=user_download_folder,installer_path=msi_center_installer_path)
    # Install MSI Center
    unzip('MSI-Center.zip', user_download_folder)
    install_program(msi_center_installer_path)

# Check if MSI Center is already installed
def check_and_launch_msi_center():
    if "Micro-Star" in mobo_manufacturer():
        try:
            with is_msi_center_installed():
                launch_msi_center()
        except FileNotFoundError:
            install_msi_center()

def msi():
    print(mobo_manufacturer())
    check_and_launch_msi_center()