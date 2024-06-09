from utilities import *
import glob

# Define the URL to download MSI Center
msi_center_download_url = "https://download.msi.com/uti_exe/desktop/MSI-Center.zip"
msi_center_assist_zip_filename = "MSI-Center.zip"
msi_center_zip_path = os.path.join(user_download_folder(), msi_center_assist_zip_filename)
# Set the installer path to the specified download folder
def is_msi_center_installed():
    cmd = 'powershell "Get-AppxPackage -AllUsers | Where-Object {$_.Name -like \'*MSICenter*\' -or $_.Name -like \'*MSIcenter*\' -or $_.Name -like \'*MSI center*\'}"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return 'MSICenter' in result.stdout or 'MSIcenter' in result.stdout or 'MSI center' in result.stdout

def install_msi_center():
    # Download and unzip the installer
    download_installer(msi_center_download_url, user_download_folder(), msi_center_zip_path)
    msi_unzip_folder = os.path.join(user_download_folder(), "MSI-Center")
    unzip(msi_center_zip_path, msi_unzip_folder)

    # Now that the .exe file has been unzipped, we can find its path
    msi_center_exe = glob.glob(os.path.join(msi_unzip_folder, "MSI-Center*.exe"))[0]
    if msi_center_exe:
        program_name = "MSI Center"
        if os.path.exists(msi_center_exe):
            try:
                subprocess.run([msi_center_exe], check=True)
                print(f"{program_name} installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error installing {program_name}: {e}")
        else:
            print("Error: Installer not found.")
    else:
        print("No MSI Center installer found in the download folder.")


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


# Check if MSI Center is already installed
def check_and_launch_msi_center():
    if is_msi_center_installed():
        launch_msi_center()
    if not is_msi_center_installed():
        install_msi_center()
        launch_msi_center()


def msi():
    print(mobo_manufacturer())
    check_and_launch_msi_center()
