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

            # Get the user's update choice
            update_choice = display_update_menu()
            # Update Dell SupportAssist
            print(wmi.WMI().Win32_ComputerSystem()[0].Manufacturer)
            if "Dell" in wmi.WMI().Win32_ComputerSystem()[0].Manufacturer and (update_choice == 1 or update_choice == 5) and is_supportassist_installed():
                launch_dell_supportassist()
                # Download the installer
                if not is_supportassist_installed():
                    response = requests.get(support_assist_download_url, stream=True)
                    if response.status_code == 200:
                        if not os.path.exists(user_download_folder):
                            os.makedirs(user_download_folder)

                        with open(support_assist_installer_path, 'wb') as installer_file:
                            for chunk in response.iter_content(chunk_size=1024):
                                installer_file.write(chunk)

                        # Install Dell SupportAssist
                        if os.path.exists(support_assist_installer_path):
                            try:
                                subprocess.run([support_assist_installer_path], check=True)
                                print("Dell SupportAssist installed successfully.")
                            except subprocess.CalledProcessError as e:
                                print(f"Error installing Dell SupportAssist: {e}")
                        else:
                            print("Error: Installer not found.")
            # Update Winget
            # Check if the user needs to accept terms for using winget
            if update_choice == 2 or update_choice == 5:
                # Upgrade all installed packages using winget
                try:
                    subprocess.run(["winget", "upgrade", "--all", "--accept-source-agreements"], check=True,)
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