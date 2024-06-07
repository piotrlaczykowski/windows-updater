import os
import sys
import ctypes
import subprocess
import requests
import wmi

# Function to display the update menu
def display_update_menu():
    print("Select an option to update:")
    print("1. Dell Support Assist")
    print("2. Winget Update")
    print("3. Choco Update")
    print("4. Windows Update")
    print("5. All")
    while True:
        choice = input("Enter your choice (1/2/3/4/5): ")
        if choice in ["1", "2", "3", "4", "5"]:
            return int(choice)
        else:
            print("Invalid choice. Please enter a valid option.")

def mobo_manufacturer():
    motherboard = wmi.WMI().Win32_ComputerSystem()[0].Manufacturer
    return motherboard

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True

    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    return False

# Check if Chocolatey (choco) is installed
def is_choco_installed():
    try:
        subprocess.run(["choco", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install Chocolatey (choco)
def install_choco():
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"], check=True)
        print("Chocolatey (choco) installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Chocolatey (choco): {e}")

# Function to upgrade packages using Chocolatey (choco)
def upgrade_choco_packages():
    try:
        subprocess.run(["choco", "upgrade", "all", "-y"], check=True)
        print("All Chocolatey packages upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading Chocolatey packages: {e}")

def download_installer(url, user_download_folder, installer_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        if not os.path.exists(user_download_folder):
            os.makedirs(user_download_folder)

        with open(installer_path, 'wb') as installer_file:
            for chunk in response.iter_content(chunk_size=1024):
                installer_file.write(chunk)

def unsecured_download_installer(url, user_download_folder, installer_path):
    try:
        response = requests.get(url, stream=True, verify=False)
        if response.status_code == 200:
            os.makedirs(user_download_folder, exist_ok=True)
            with open(installer_path, 'wb') as installer_file:
                for chunk in response.iter_content(chunk_size=1024):
                    installer_file.write(chunk)
            print(f"Downloaded installer to {installer_path}")
        else:
            print(f"Error downloading installer: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

def install_program(installer_path):
    if os.path.exists(installer_path):
        try:
            subprocess.run([installer_path], check=True)
            print("Dell SupportAssist installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing Dell SupportAssist: {e}")
    else:
        print("Error: Installer not found.")
        
def winget_upgrade():
    # Upgrade all installed packages using winget
    try:
        subprocess.run(["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements", "-u", "--allow-reboot"], check=True,)
        print("All installed packages upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading packages with winget: {e}")
        
def choco_upgrade():
    if not is_choco_installed():
        print("Chocolatey (choco) is not installed. Installing it now...")
        install_choco()
        try:
            subprocess.run(["choco", "upgrade", "all", "-y"], check=True)
            print("All Chocolatey packages upgraded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error upgrading Chocolatey packages: {e}")

def windows_update():
    try:
        print("Checking for Windows updates...")

        # Install the PSWindowsUpdate module if not already installed
        ps_install_command = (
            "Install-Module PSWindowsUpdate -Force -AllowClobber -Scope AllUsers; "
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "Import-Module PSWindowsUpdate -Force;"
            "$serviceManager = New-Object -ComObject 'Microsoft.Update.ServiceManager';"
            "$serviceManager.AddService2('7971f918-a847-4430-9279-4a52d1efe18d',7,'');"
            "Install-WindowsUpdate -AcceptAll -AutoReboot -IgnoreUserInput;"
        )

        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_install_command], check=True)

        print("Windows updates checked and installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error checking or installing Windows updates: {e}")
