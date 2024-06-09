from motherboard import *
from utilities import *

if __name__ == "__main__":
    if run_as_admin():
        try:
            update_choice = display_update_menu()
            if update_choice == 1 or update_choice == 5:
                motherboard_launcher()
            # Update Winget
            # Check if the user needs to accept terms for using winget
            if update_choice == 2 or update_choice == 5:
                winget_upgrade()

            # Check if Chocolatey (choco) is installed and perform the necessary actions
            if update_choice == 3 or update_choice == 5:
                choco_upgrade()

            # Update Windows
            if update_choice == 4 or update_choice == 5:
                windows_update()

            # End of the script
            print("Script execution completed.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            input("Press Enter to exit...")
    else:
        sys.exit(0)