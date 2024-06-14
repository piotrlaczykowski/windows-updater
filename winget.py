import subprocess

def winget_upgrade():
    # Upgrade all installed packages using winget
    try:
        subprocess.run(["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements", "--allow-reboot"], check=True,)
        print("All installed packages upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading packages with winget: {e}")
