import os
import subprocess
import tkinter as tk
import requests
import shutil
import zipfile
import io
import json
import sys
import threading
import pygame
import time
import random
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

VERSION_NUMBER = "v1.00"
CONSOLE = 1
CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "Balatro_EMI_config.json")

# Get current user and set default download location
current_user = os.getlogin()
default_mods_folder = f"C:/Users/{current_user}/AppData/Roaming/Balatro/Mods"
mods_folder = default_mods_folder

# Global variables for file paths
default_balatro_folder = "C:/Program Files (x86)/Steam/steamapps/common/Balatro/"
balatro_folder = default_balatro_folder
lovely_dll = "version.dll"
balatro_exe = "Balatro.exe"
lovely_path = balatro_folder + lovely_dll
balatro_exe_path = balatro_folder + balatro_exe

# Color variables for status
CHIPS_BLUE = "#009DFF"
MULT_RED = "#FF4C40"
CASHOUT_YELLOW = "#F5B244"
COLLECTION_GREEN = "#35BD86"
CHIPS_BLUE_PRESSED = "#0057A1"
MULT_RED_PRESSED = "#A02721"
CASHOUT_YELLOW_PRESSED = "#A05B00"
COLLECTION_GREEN_PRESSED = "#215F46"

# Mod Downloading Stuff
LOVELY_GITHUB = "ethangreen-dev/lovely-injector"
STEAMODDED_GITHUB = "Steamodded/smods"
DECK_CREATOR_GITHUB = "adambennett/Balatro-DeckCreator"
MULTIPLAYER_GITHUB = "V-rtualized/BalatroMultiplayer"
UPDATE_API_URL = "https://api.github.com/repos/Scary-Branden/Balatro_EMI/releases/latest"

if getattr(sys, 'frozen', False):  
    # If running as an executable, use the folder where the .exe is located
    base_path = os.path.dirname(sys.argv[0])  # Get the directory of the .exe
else:
    # If running as a script, use the directory where the script is located
    base_path = os.path.dirname(os.path.abspath(__file__))

# Path to store the downloaded .exe
#script_dir = Path(__file__).parent
exe_path = os.path.join(base_path, "EMI Updater.exe")  # Change this if needed

# Path to your icon file
icon_path = "resources/madness.ico"
# Initialize Tkinter window
root = tk.Tk()
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)  # Set the window icon if the file exists
#else:
    #messagebox.showwarning("Icon not found", "Icon file not found, using default icon.")
root.title(f"Balatro EMI {VERSION_NUMBER}")
#root.iconbitmap("resources/madness.ico")
root.geometry("320x160")  # Adjust window size
# Set a global font for all widgets
root.option_add("*Font", ("m6x11plus", 12))
root.option_add("*Foreground", "white")                  # Text color (foreground)
root.option_add("*Background", "#18252A")                  # Text color (foreground)

# Status variables
status_var = tk.StringVar()

# Declare status_label as global so it's accessible in multiple functions
global status_label

# Function to determine the current status on startup
def check_status():
    print("Checking status...")  # Debugging
    if os.path.exists(lovely_path):
        status_var.set("Lovely Enabled")
        status_label.config(bg=MULT_RED)
    else:
        status_var.set("Lovely Disabled")
        status_label.config(bg=CHIPS_BLUE)

def check_and_download_latest():
    """Check version and download the latest .exe if outdated."""
    try:
        # Get the latest version from GitHub
        response = requests.get(UPDATE_API_URL)
        response.raise_for_status()
        release_data = response.json()

        latest_version = release_data["tag_name"]  # Version from GitHub
        print(f"Latest: {latest_version} | Current: {VERSION_NUMBER}")

        # Compare versions
        if latest_version != VERSION_NUMBER:
            print("New update available! Downloading...")

            # Run the latest .exe
            if os.path.exists(exe_path):
                response = messagebox.askyesno("EMI Updater", "Update found!\nWould you like to download the latest version of EMI?")
                if response:
                    subprocess.Popen([str(exe_path)], shell=True)
                    sys.exit(0)  # Gracefully exit the program
            else:
                print(f"Executable not found at {exe_path}")

        else:
            print("Already up to date.")

        

    except Exception as e:
        print(f"Error checking/updating version: {e}")

# Rename file function
def rename_file(option):
    print(f"Renaming file to {option}...")  # Debugging
    if option == "enabled":
        new_name = lovely_path
    else:
        new_name = lovely_path + ".disabled"

    try:
        if os.path.exists(lovely_path + ".disabled"):
            file_path = lovely_path + ".disabled"
        else:
            file_path = lovely_path

        if file_path != new_name and os.path.exists(file_path):
            os.rename(file_path, new_name)
            print(f"File renamed to: {new_name}")
    except Exception as e:
        print(f"Error: {e}")

# Launch program function
def launch_program():
    print("Launching the program...")  # Debugging
    try:
        subprocess.Popen([balatro_exe_path], shell=True)
        # subprocess.run([balatro_exe_path], shell=True)
        while pygame.mixer.get_busy():
            time.sleep(0.1)
        sys.exit(0)  # Gracefully exit the program
        # os._exit(0)  # Forcefully exit the program
    except Exception as e:
        print(f"Error launching program: {e}")

# Hide the console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), CONSOLE)

# Button functions for each option
def enable_mods():
    if pygame.mixer.get_busy():
        play("multhit2")

    # Check if version.dll or version.dll.disabled exists
    if not os.path.exists(lovely_path) and not os.path.exists(lovely_path + ".disabled"):
        # If neither file exists, show "No Lovely Installed" for 5 seconds
        status_var.set("No Lovely Installed")
        status_label.config(bg=CASHOUT_YELLOW)  # Optional: different color for this status

        # After 5 seconds, reset status back to "Mods Enabled"
        root.after(2000, disable_mods)
    else:
        # If version.dll exists, set the status as "Mods Enabled"
        rename_file("enabled")
        status_var.set("Lovely Enabled")
        status_label.config(bg=MULT_RED)

def disable_mods():
    rename_file("disabled")
    status_var.set("Lovely Disabled")
    status_label.config(bg=CHIPS_BLUE)

def prepare_lovely_download(mod_name, repo_owner_and_name, download_path):
    dll_path = os.path.join(download_path, "version.dll")
    disabled_dll_path = dll_path + ".disabled"

    # If version.dll.disabled exists, delete it
    if os.path.exists(disabled_dll_path):
        os.remove(disabled_dll_path)
        print("Deleted version.dll.disabled")

    # Now proceed with downloading version.dll as usual
    download_and_extract_mods_threaded(mod_name, repo_owner_and_name, download_path)

# Function to download and extract mods with threading
def download_and_extract_mods_threaded(mod_name, repo_owner_and_name, download_path):
    thread = threading.Thread(target=download_and_extract_mods, args=(mod_name, repo_owner_and_name, download_path))
    thread.start()

# Modify the download_and_extract_mods function to update the GUI during the download and extraction process
def download_and_extract_mods(mod_name, repo_owner_and_name, download_path):
    print(f"Fetching {mod_name}...")  # Debugging
    if mod_name == "Lovely":
        dll_path = os.path.join(download_path, "version.dll")
        disabled_dll_path = dll_path + ".disabled"

        # If version.dll.disabled exists, delete it
        if os.path.exists(disabled_dll_path):
            os.remove(disabled_dll_path)
            print("Deleted version.dll.disabled")

    try:
        status_var.set(f"Downloading {mod_name}...")  # Update status for download
        status_label.config(bg=CASHOUT_YELLOW)

        # If source_code is False, get the latest release from the GitHub API
        api_url = f"https://api.github.com/repos/{repo_owner_and_name}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        release_data = response.json()

        # Extract version information from the release
        version = release_data['tag_name']  # This is usually the version number

        # Find the correct asset (usually a .zip file) in the release data
        download_url = None
        for asset in release_data.get('assets', []):
            if '.zip' in asset['name']:
                download_url = asset['browser_download_url']
                print(f"Found asset: {asset['name']}")
                break

        if not download_url:
            download_url = f"https://github.com/{repo_owner_and_name}/archive/refs/heads/main.zip"
            print(f"Downloading source code from: {download_url}")
            version = "Source Code (main branch)"
                
            if not download_url:
                status_var.set(f"No valid asset for {mod_name}.")
                print(f"No matching asset found for {mod_name}.")
                return

        print(f"Downloading from: {download_url}")

        # Display the version in the status bar
        status_var.set(f"{mod_name} {version} - Downloading...")

        # Start downloading the file
        file_response = requests.get(download_url, stream=True)
        file_response.raise_for_status()

        # Update status to show the download is happening
        status_var.set(f"Extracting {mod_name}...")

        # Extract the ZIP file
        if download_url.lower().endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(file_response.content)) as zip_ref:
                # Get list of files in the zip
                file_names = zip_ref.namelist()

                # Check if there are multiple files at the root of the zip
                if len([file for file in file_names if file.count('/') == 0]) > 1:
                    # Create a folder if there are multiple root-level files
                    folder_name = os.path.join(download_path, mod_name)
                    os.makedirs(folder_name, exist_ok=True)
                    # Extract all files to that folder
                    zip_ref.extractall(folder_name)
                else:
                    # If there's only one file or a directory structure, extract normally
                    zip_ref.extractall(download_path)

        elif download_url.lower().endswith('.tar.gz'):
            import tarfile
            with tarfile.open(fileobj=io.BytesIO(file_response.content), mode="r:gz") as tar_ref:
                tar_ref.extractall(download_path)

        status_var.set(f"{mod_name} {version} installed!")
        status_label.config(bg=CHIPS_BLUE)

        mod_version = get_mod_version(mod_name)

        if mod_version:
            print(f"The MF version of {mod_name} is {version}")
        else:
            print(f"{mod_name} not found in the MF config.")

        print(f"{mod_name} downloaded to: {download_path}")
        update_mod_version(mod_name, version)

    except Exception as e:
        status_var.set("Error Downloading Mods")
        status_label.config(bg=MULT_RED)
        print(f"Error: {e}")

# Function to get the version of a specific mod from config
def get_mod_version(mod_name):
    mod_versions = load_config()  # Load the config and get mod versions
    return mod_versions.get(mod_name, "Version not found")

# Function to update button text with mod version
def update_button_with_version(button, mod_name):
    version = get_mod_version(mod_name)
    button.config(text=f"{mod_name}: {version}")

# Function to load the existing config and load mod versions
def load_config():
    global balatro_folder, mods_folder
    print("LOADING CONFIG")
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            
            # Always load the paths from the config file
            balatro_folder = config.get("balatro_folder", balatro_folder)
            mods_folder = config.get("mods_folder", mods_folder)

            # Return mod_versions as well
            return config.get('mod_versions', {})
    except FileNotFoundError:
        # If the config file doesn't exist, return empty mod_versions dict
        return {}

# Function to save the config, including mod versions and folder paths
def save_config(save_paths=False, mod_versions=None):
    try:
        # Load the existing config if it exists, otherwise initialize an empty one
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        else:
            config = {}

        # Update paths if needed
        if save_paths:
            config["balatro_folder"] = balatro_folder
            config["mods_folder"] = mods_folder
            status_var.set(f"Path locations saved!")
            status_label.config(bg=CHIPS_BLUE)

            if config["balatro_folder"] is default_balatro_folder:
                del config["balatro_folder"]
                print("'balatro_folder' key removed from the configuration.")

            if config["mods_folder"] is default_mods_folder:
                del config["mods_folder"]
                print("'mods_folder' key removed from the configuration.")

        # Update mod versions if provided (merge with existing)
        if mod_versions:
            if "mod_versions" not in config:
                config["mod_versions"] = {}
            
            # Merge new mod versions with existing ones
            config["mod_versions"].update(mod_versions)

        # Save the updated config to the JSON file
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

        print(f"Config saved to {CONFIG_FILE}")
    
    except Exception as e:
        print(f"Error saving config: {e}")


# Function to update mod version info in the config
def update_mod_version(mod_name, version):
    # Load the existing config
    config = load_config()

    # Ensure 'mod_versions' exists in the config, if not, initialize it
    mod_versions = config.get("mod_versions", {})

    # Update or add the mod version
    mod_versions[mod_name] = version

    # Save the updated config
    save_config(save_paths=False, mod_versions=mod_versions)
    print(f"Mod version for {mod_name} updated to {version}")

# Function to reset the game location to the default path
def reset_path_locations():
    global balatro_folder, mods_folder
    balatro_folder = default_balatro_folder
    game_location_entry.config(state="normal")  # Temporarily enable the entry
    game_location_entry.delete(0, tk.END)  # Clear the entry
    game_location_entry.insert(0, balatro_folder)  # Insert the default path
    game_location_entry.config(state="disabled")  # Disable it again
    print(f"Game location reset to: {balatro_folder}")

    mods_folder = default_mods_folder
    mods_location_entry.config(state="normal")  # Temporarily enable the entry
    mods_location_entry.delete(0, tk.END)  # Clear the entry
    mods_location_entry.insert(0, mods_folder)  # Insert the default path
    mods_location_entry.config(state="disabled")  # Disable it again
    print(f"Mods location reset to: {mods_folder}")


    status_var.set(f"Path locations reset! Please save")
    status_label.config(bg=CASHOUT_YELLOW)

# Function to allow the user to change the download location using a file explorer
def set_path_location(path_location, location_entry, folder_name):
    global balatro_folder, mods_folder  # Make sure to access globals

    print(f"Opening file explorer for {folder_name}...")  # Debugging
    selected_folder = filedialog.askdirectory(initialdir=path_location, title=f"Select {folder_name} Folder")

    if selected_folder:
        if folder_name == "Balatro":
            balatro_folder = selected_folder  # Update balatro_folder
        elif folder_name == "Mods":
            mods_folder = selected_folder  # Update mods_folder

        location_entry.config(state="normal")  # Temporarily enable the entry
        location_entry.delete(0, tk.END)  # Clear the entry
        location_entry.insert(0, selected_folder)  # Insert the new path
        location_entry.config(state="disabled")  # Disable it again

        # Save the updated paths
        #save_config()

        print(f"New {folder_name} location set to: {selected_folder}")

def play(sound, sound_max="", file_type=".ogg"):

    #status_var.set(f"Sound played!")
    #status_label.config(bg=CASHOUT_YELLOW)
    if sound_max != "":
        sound_number = random.randint(1, sound_max)
    else:
        sound_number = sound_max

    sound_path = f"resources/sounds/{sound}{sound_number}{file_type}"
    pygame.mixer.Sound(sound_path).play()
    print(f"Playing: {sound_path}")

# Create the frames for each "page"
home_frame = tk.Frame(root)
download_frame = tk.Frame(root)

# Add widgets for the Home Page (Main page)
def setup_home_frame():
    print("Setting up home frame...")  # Debugging
    # Enable Mods button
    enable_button = tk.Button(home_frame, text="Enable Mods", bg=MULT_RED, activeforeground="white", activebackground=MULT_RED_PRESSED, command=lambda: (enable_mods(), play("multhit1")), width=15, height=2)
    enable_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Play Vanilla button
    disable_button = tk.Button(home_frame, text="Vanilla", bg=CHIPS_BLUE, activeforeground="white", activebackground=CHIPS_BLUE_PRESSED, command=lambda: (disable_mods(), play("chips1")), width=15, height=2)
    disable_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Launch Balatro button
    launch_button = tk.Button(home_frame, text="Launch Balatro", bg=COLLECTION_GREEN, activeforeground="white", activebackground=COLLECTION_GREEN_PRESSED, command=lambda: (play("glass", 6), launch_program()), width=15, height=2)
    launch_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Button to go to the download page
    download_button = tk.Button(home_frame, text="Install Mods", bg=CASHOUT_YELLOW, activeforeground="white", activebackground=CASHOUT_YELLOW_PRESSED, command=lambda: (switch_to_frame(download_frame), play("whoosh")), width=15, height=2)
    download_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Ensure both columns have equal weight for resizing
    home_frame.grid_columnconfigure(0, weight=1, uniform="equal")
    home_frame.grid_columnconfigure(1, weight=1, uniform="equal")

# Add widgets for the Download Page
def setup_download_frame():
    print("Setting up download frame...")  # Debugging
    # Game Location Widgets
    game_location_label = tk.Label(download_frame, text="Game Location:")
    game_location_label.grid(row=0, column=0, columnspan=2, padx=10, pady=0, sticky="w")

    global game_location_entry
    game_location_entry = tk.Entry(download_frame, width=30)
    game_location_entry.insert(0, balatro_folder)  # Default to current path
    game_location_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

    # Set Location button
    update_game_location_button = tk.Button(download_frame, text="Browse...", bg=CHIPS_BLUE, activeforeground="white", activebackground=CHIPS_BLUE_PRESSED, command=lambda: (play("cardSlide1"), set_path_location(balatro_folder, game_location_entry, "Balatro")), width=15, height=2)
    update_game_location_button.grid(row=1, column=3, columnspan=1, padx=10, pady=4, sticky="nsew")

    # Reset Location button
    reset_paths_location_button = tk.Button(download_frame, text="Reset", bg=COLLECTION_GREEN, activeforeground="white", activebackground=COLLECTION_GREEN_PRESSED, command=lambda: (reset_path_locations(), play("timpani")), width=10, height=2)
    reset_paths_location_button.grid(row=1, column=4, columnspan=1, padx=10, pady=4, sticky="nsew")

    # Download Location Widgets
    mods_location_label = tk.Label(download_frame, text="Mods Location:")
    mods_location_label.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky="w")

    global mods_location_entry
    mods_location_entry = tk.Entry(download_frame, width=30)
    mods_location_entry.insert(0, mods_folder)  # Default to current path
    mods_location_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

    # Set Location button
    update_mods_location_button = tk.Button(download_frame, text="Browse...", bg=CHIPS_BLUE, activeforeground="white", activebackground=CHIPS_BLUE_PRESSED, command=lambda: (play("cardSlide1"), set_path_location(mods_folder, mods_location_entry, "Mods")), width=15, height=2)
    update_mods_location_button.grid(row=3, column=3, columnspan=1, padx=10, pady=4, sticky="nsew")

    # Reset Location button
    save_paths_button = tk.Button(download_frame, text="Save", bg=COLLECTION_GREEN, activeforeground="white", activebackground=COLLECTION_GREEN_PRESSED, command=lambda: (save_config(True, None), play("coin", 7)), width=10, height=2)
    save_paths_button.grid(row=3, column=4, columnspan=1, padx=10, pady=4, sticky="nsew")

    # Disable editing in the path location entries
    game_location_entry.config(state="disabled")
    mods_location_entry.config(state="disabled")

    # Define the mods and their associated GitHub URLs and sounds
    mods_info = {
        "Lovely": {"version": [""], "github_url": LOVELY_GITHUB, "dl_folder": balatro_folder, "sound": "holo1"},
        "Steamodded": {"version": [""], "github_url": STEAMODDED_GITHUB, "dl_folder": mods_folder, "sound": "polychrome1"},
        "Deck Creator": {"version": [""], "github_url": DECK_CREATOR_GITHUB, "dl_folder": mods_folder, "sound": "foil1"},
        "Multiplayer": {"version": [""], "github_url": MULTIPLAYER_GITHUB, "dl_folder": mods_folder, "sound": "negative"}
    }

    # Loop through mods_info and create buttons dynamically
    # Start position for buttons
    start_row = 4  
    columns_per_row = 2  # Number of columns before wrapping to next row
    for index, (mod_name, mod_info) in enumerate(mods_info.items()):
        # Calculate row and column dynamically
        row = start_row + (index // columns_per_row)  # Increase row every 2 buttons
        column = index % columns_per_row + 1          # Alternate between 1 and 2
        columnspan = column * 2 - 1

        download_button = tk.Button(
            download_frame,
            text=f"{mod_name} {mod_info['version']}",
            bg=MULT_RED,
            activeforeground="white",
            activebackground=MULT_RED_PRESSED,
            command=lambda mod_name=mod_name, mod_info=mod_info: (download_and_extract_mods_threaded(mod_name, mod_info['github_url'], mod_info['dl_folder']), play(mod_info['sound'])),
            width=30,
            height=2
        )
        download_button.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=10, sticky="nsew")

    # Download Lovely button
    #download_button = tk.Button(download_frame, text="Lovely {lovely_version}", bg=MULT_RED, activeforeground="white", activebackground=MULT_RED_PRESSED, command=lambda: (download_and_extract_mods_threaded("Lovely", LOVELY_GITHUB, balatro_folder), play("holo1")), width=30, height=2)
    #download_button.grid(row=4, column=1, columnspan=1, padx=10, pady=10, sticky="nsew")

    # Download Steamodded button
    #download_button = tk.Button(download_frame, text="Steamodded {steamodded_version}", bg=MULT_RED, activeforeground="white", activebackground=MULT_RED_PRESSED, command=lambda: (download_and_extract_mods_threaded("Steamodded", STEAMODDED_GITHUB, mods_folder), play("polychrome1")), width=30, height=2)
    #download_button.grid(row=4, column=2, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Download Deck Creator button
    #download_button = tk.Button(download_frame, text="Deck Creator {deck_creator_version}", bg=MULT_RED, activeforeground="white", activebackground=MULT_RED_PRESSED, command=lambda: (download_and_extract_mods_threaded("Deck Creator", DECK_CREATOR_GITHUB, mods_folder), play("foil1")), width=30, height=2)
    #download_button.grid(row=5, column=1, columnspan=1, padx=10, pady=10, sticky="nsew")

    # Download Multiplayer button
    #download_button = tk.Button(download_frame, text="Multiplayer {multiplayer_version}", bg=MULT_RED, activeforeground="white", activebackground=MULT_RED_PRESSED, command=lambda: (download_and_extract_mods_threaded("Multiplayer", MULTIPLAYER_GITHUB, mods_folder), play("negative")), width=30, height=2)
    #download_button.grid(row=5, column=2, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Button to go back to the home page
    back_button = tk.Button(download_frame, text="Back", bg=CASHOUT_YELLOW, activeforeground="white", activebackground=CASHOUT_YELLOW_PRESSED, command=lambda: (switch_to_frame(home_frame), play("whoosh")), width=30, height=2)
    back_button.grid(row=5, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")

    # Make the first column wider than the second for the first 4 rows
    download_frame.grid_columnconfigure(0, weight=3, uniform="equal")  # First column takes more space
    download_frame.grid_columnconfigure(1, weight=7, uniform="equal")  # Second column takes less space
    download_frame.grid_columnconfigure(2, weight=2, uniform="equal")  # First column takes more space
    download_frame.grid_columnconfigure(3, weight=3, uniform="equal")  # Second column takes less space
    download_frame.grid_columnconfigure(4, weight=2, uniform="equal")  # First column takes more space
    download_frame.grid_rowconfigure(0, weight=1, uniform="equal")
    download_frame.grid_rowconfigure(1, weight=1, uniform="equal")
    download_frame.grid_rowconfigure(2, weight=1, uniform="equal")
    download_frame.grid_rowconfigure(3, weight=1, uniform="equal")
    download_frame.grid_rowconfigure(4, weight=2, uniform="equal")
    download_frame.grid_rowconfigure(5, weight=2, uniform="equal")

# Create the global status bar at the bottom of the window
status_label = tk.Label(root, textvariable=status_var, relief="sunken", anchor="w", padx=10)
status_label.grid(row=1, column=0, columnspan=1, sticky="ew")

# Ensure the status bar remains at the bottom by configuring row weights
root.grid_rowconfigure(0, weight=1)  # Main content area (frames)
root.grid_rowconfigure(1, weight=0)  # Status bar (fixed size)
root.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion
root.resizable(False, False)  # Disable manual resizing

# Ensure that the window will adjust dynamically when switching between frames
home_frame.grid_rowconfigure(0, weight=0)  # Make home_frame size static
home_frame.grid_columnconfigure(0, weight=1)

download_frame.grid_rowconfigure(0, weight=0)  # Make download_frame expand dynamically
download_frame.grid_rowconfigure(1, weight=0)  # Adjust second row height
download_frame.grid_columnconfigure(0, weight=1)

# Allow frames to propagate their sizes (i.e., dynamically adjust based on content)
home_frame.grid_propagate(True)  # Allow home_frame to resize
download_frame.grid_propagate(True)  # Allow download_frame to resize

# Set frames to expand and fill the available space
home_frame.grid(row=0, column=0, sticky="nsew")
download_frame.grid(row=0, column=0, sticky="nsew")

# Adjust the window size based on the content of the current active frame
def switch_to_frame(frame):
    print(f"Switching to frame: {frame}")  # Debugging
    frame.tkraise()  # Bring the selected frame to the front

    # Dynamically adjust the window size based on the current frame's content
    if frame == download_frame:
        root.geometry("600x280")  # Example for larger frame (adjust as needed)
        
    else:
        root.geometry("320x160")  # Default size for home_frame (adjust as needed)
        check_status()

# Set weight of rows and columns so they expand properly
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Load saved paths on startup
load_config()

check_and_download_latest()

# Setup frames
setup_home_frame()
setup_download_frame()

# Check the status on startup
check_status()

# Initialize the mixer
pygame.mixer.init()

# Raise the home frame first (this will be the default view)
home_frame.tkraise()

# Run the Tkinter event loop
root.mainloop()
