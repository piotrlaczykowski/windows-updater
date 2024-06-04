import os
import sys
import ctypes
import subprocess
import winreg

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


def launch_dell_supportassist():
    try:
        ps_command = (
            "Get-AppxPackage | Where-Object {$_.Name -like 'DellSupportAssist'} | "
            "Foreach-Object {"
            "$packageName = $_.PackageFamilyName;"
            "Start-Process shell:AppsFolder\\$packageName!App;"
            "}"
        )
        subprocess.run(["powershell", "-Command", ps_command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching the UWP app: {e}")

# Check if Dell SupportAssist is already installed
def is_supportassist_installed():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Dell\SupportAssistAgent", 0, winreg.KEY_READ) as key:
            return True
    except FileNotFoundError:
        return False