import os
from glob import glob
from pathlib import Path
import tkinter
from tkinter import filedialog
from datetime import datetime, timedelta
import webbrowser
from config import glob_locations


class OutputColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_previous_sunday():
    today = datetime.today()
    # Calculate the number of days to subtract to get to the previous Sunday
    days_to_subtract = today.weekday() + 1  # Adding 1 because Monday is 0
    previous_sunday = today - timedelta(days=days_to_subtract)
    return previous_sunday


def get_upcoming_friday():
    today = datetime.today()
    # Calculate the number of days to add to get to the upcoming Friday
    days_to_add = (4 - today.weekday() + 7) % 7  # Adding 7 to ensure positive remainder
    upcoming_friday = today + timedelta(days=days_to_add)
    return upcoming_friday


move_locations = {
    "Action Folder": r"C:\Users\codym\OneDrive\Action Folder",
    "Reeds UMC Action Folder": r"C:\Users\codym\OneDrive\Reeds UMC\Reeds Action Folder",
    "Payroll": r"C:\Users\codym\Dropbox\Data Storage\My Documents\Apartments\Koontz & Goforth\HR\Payroll\2024",
    "previous": ""
}


# Get All files in directory
def get_files(default_locations=glob_locations):
    input_string = "What folder would you like to clear:\n"
    for index, key in enumerate(default_locations):
        if default_locations[key][0] != "":
            input_string = input_string + f"{index + 1} - {default_locations[key][0]}" + "\n"
    # input_string += input_string + "9 - Other\n"
    location_input = input(input_string)

    match location_input.lower():
        case '1':
            return glob(glob_locations["location_1"][1])
        case '2':
            return glob(glob_locations["location_2"][1])
        case "9":
            tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
            folder_path = filedialog.askdirectory()
            glob_path = folder_path + "\\*"
            return glob(glob_path)


def move_file(file_path, file_name):
    location_choice = input("Where would you like to move the file to: \n"
                            "1 - Action folder\n"
                            "2 - Reeds UMC Action\n"
                            "3 - Payroll - current week\n"
                            "8 - Previously Selected Location\n"
                            "9 - Select location\n")

    match location_choice:
        case '1':
            new_path = move_locations['Action Folder'] + "\\" + file_name
            os.rename(file_path, new_path)
            print("File moved to Action Folder")
        case '2':
            new_path = move_locations['Reeds UMC Action Folder'] + "\\" + file_name
            os.rename(file_path, new_path)
            print("File moved to Reeds UMC Action Folder")
        case '3':
            friday = get_upcoming_friday().strftime("%Y-%m-%d")
            payroll_folder_path = Path(move_locations['Payroll'], friday)
            if not payroll_folder_path.exists():
                os.makedirs(payroll_folder_path)
            payroll_path = Path(payroll_folder_path, file_name)
            os.rename(file_path, payroll_path)
            print(f"Payroll for {friday}")
        case '8':
            new_path = move_locations['previous'] + "\\" + file_name
            os.rename(file_path, new_path)
            print("File moved to Action Folder")
        case '9':
            tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
            folder_path = filedialog.askdirectory()
            move_locations['previous'] = folder_path
            new_path = folder_path + "\\" + file_name
            os.rename(file_path, new_path)
            print("new folder path " + folder_path)

    print(f"{file_name} File Moved")


def rename_file(file_path, file_name_to_change):
    new_name = input(f"What would you like to rename {file_name_to_change}: ")
    new_path = file_path.replace(file_name_to_change, new_name)
    # print(new_path)
    os.rename(file_path, new_path)
    print(f"{new_path} was renamed")
    return new_path


def delete_file(file_path):
    try:
        # Attempt to remove the file
        os.remove(file_path)
        print("File deleted successfully.")
    except OSError as e:
        # Handle errors, if any
        print(f"Error: {file_path} - {e.strerror}")


def preview_file(file_path):
    webbrowser.open('file://' + file_path)


if __name__ == "__main__":
    exit_app = False
    files = get_files()
    for file in files:
        while True:
            file_name_with_ext = Path(file).stem
            file_name_no_ext = Path(file).name
            action = input(
                f"\nWhat would you like to do with {OutputColors.WARNING}{file_name_no_ext}{OutputColors.ENDC}\n"
                "[m]ove, [r]ename, [d]elete, [s]kip, [p]review, or [q]uit ")
            match action.lower():
                case 'm':
                    move_file(file, file_name_no_ext)
                    break
                case "r":
                    file = rename_file(file, file_name_with_ext)
                    continue
                case 'd':
                    delete_file(file)
                    break
                case 'p':
                    preview_file(file)
                    continue
                case 's':
                    break
                case 'q':
                    exit_app = True
                    break
        if exit_app:
            break

    print('Download folder empty!!')
