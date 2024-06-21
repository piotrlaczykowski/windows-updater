import subprocess

def is_winget_installed():
    try:
        subprocess.run(["winget", "--version"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def install_winget():
    try:
        subprocess.run(["powershell", "-Command", "Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe"], check=True)
        print ("Winget is installed")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Winget: {e}")

def upgrade_winget_packages():
    # Upgrade all installed packages using winget
    try:
        subprocess.run(["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements", "--allow-reboot"], check=True,)
        print("All installed packages upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading packages with winget: {e}")

def winget_upgrade():
    if not is_winget_installed():
        print("Winget is not installed. Installing it now...")
        install_winget()
        if is_winget_installed():
            upgrade_winget_packages()
    else:
        upgrade_winget_packages()