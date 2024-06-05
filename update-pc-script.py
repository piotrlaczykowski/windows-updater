import os
import sys
import subprocess
import wmi
import requests
from utilities import *

if __name__ == "__main__":
    if run_as_admin():
        try:
            # Define the URL to download Dell SupportAssist
            support_assist_download_url = "https://downloads.dell.com/serviceability/catalog/SupportAssistInstaller.exe"

            # Set the installer path to the specified download folder
            user_download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            dell_support_assist_installer_filename = "SupportAssistInstaller.exe"
            support_assist_installer_path = os.path.join(user_download_folder, dell_support_assist_installer_filename)
            mobo_manufacturer = wmi.WMI().Win32_ComputerSystem()[0].Manufacturer
            # Get the user's update choice
            update_choice = display_update_menu()
            # Update Dell SupportAssist
            print(mobo_manufacturer)
            if "Dell" in mobo_manufacturer and (update_choice == 1 or update_choice == 5) and is_support_assist_installed():
                launch_dell_support_assist()
                # Download the installer
                if not is_support_assist_installed():
                    download_installer(url=support_assist_download_url, user_download_folder=user_download_folder,installer_path=support_assist_installer_path)
                    # Install Dell SupportAssist
                    install_program(support_assist_installer_path)
            # Update Winget
            # Check if the user needs to accept terms for using winget
            if update_choice == 2 or update_choice == 5:
                # Upgrade all installed packages using winget
                try:
                    subprocess.run(["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements", "-u", " --allow-reboot"], check=True,)
                    print("All installed packages upgraded successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error upgrading packages with winget: {e}")

            # Check if Chocolatey (choco) is installed and perform the necessary actions
            if update_choice == 3 or update_choice == 5:
                try:
                    print("Checking for Choco updates...")
                    subprocess.run(["choco", "upgrade", "all", "-y"], check=True)
                    print("All Chocolatey packages upgraded successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error upgrading Chocolatey packages: {e}")
                    if not is_choco_installed():
                        print("Chocolatey (choco) is not installed. Installing it now...")
                        install_choco()
                        try:
                            subprocess.run(["choco", "upgrade", "all", "-y"], check=True)
                            print("All Chocolatey packages upgraded successfully.")
                        except subprocess.CalledProcessError as e:
                            print(f"Error upgrading Chocolatey packages: {e}")


            # Update Windows
            if update_choice == 4 or update_choice == 5:
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

            # End of the script
            print("Script execution completed.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            input("Press Enter to exit...")
    else:
        sys.exit(0)  # Exit if user declines admin privileges