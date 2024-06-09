from utilities import * 
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
        
def choco_upgrade():
    if not is_choco_installed():
        print("Chocolatey (choco) is not installed. Installing it now...")
        install_choco()
        upgrade_choco_packages()
    else:
        upgrade_choco_packages()