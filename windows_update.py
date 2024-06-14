import subprocess

def windows_update():
    try:
        print("Checking for Windows updates...")

        # Install the PSWindowsUpdate module if not already installed
        ps_install_command = (
            "Install-PackageProvider -Name NuGet -Force;"
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
