import os
import subprocess
import tkinter as tk
import sys

# Global variables for file paths
base_file_path = "C:/Program Files (x86)/Steam/steamapps/common/Balatro/"
enabler_file = "version.dll"
game_file = "Balatro.exe"
enabler_file_path = base_file_path + enabler_file
game_file_path = base_file_path + game_file

# Color variables for status (easy to change)
VANILLA_COLOR = "#009DFF"  # Bright green for Play Vanilla
MODS_ENABLED_COLOR = "#FF4C40"  # Red for Mods Enabled

# Initialize Tkinter window
root = tk.Tk()
root.title("Balatro Mods Enabler")
root.geometry("400x200")  # Set window size to 400x200 pixels

# Status variable
status_var = tk.StringVar()

# Function to determine the current status on startup
def check_status():
    # If the .disabled file exists, mods are disabled
    if os.path.exists(enabler_file_path + ".disabled"):
        status_var.set("Play Vanilla")
        status_label.config(bg=VANILLA_COLOR)  # Use the vanilla color
    else:
        status_var.set("Mods Enabled")
        status_label.config(bg=MODS_ENABLED_COLOR)  # Use the mods enabled color

# Rename file function
def rename_file(option):
    if option == "enabled":
        new_name = enabler_file_path
    else:
        new_name = enabler_file_path + ".disabled"

    try:
        if os.path.exists(enabler_file_path + ".disabled"):
            file_path = enabler_file_path + ".disabled"
        else:
            file_path = enabler_file_path

        # Rename only if the file is different and exists
        if file_path != new_name and os.path.exists(file_path):
            os.rename(file_path, new_name)
            print(f"File renamed to: {new_name}")
    except Exception as e:
        print(f"Error: {e}")

# Launch program function
def launch_program():
    try:
        subprocess.run([game_file_path], shell=True)
        
        # Ensure status color is updated on launch
        if os.path.exists(enabler_file_path + ".disabled"):
            status_label.config(bg=VANILLA_COLOR)  # Green for Vanilla
            status_var.set("Play Vanilla")
        else:
            status_label.config(bg=MODS_ENABLED_COLOR)  # Red for Mods enabled
            status_var.set("Mods Enabled")
        
    except Exception as e:
        print(f"Error launching program: {e}")

# Button functions for each option
def enable_mods():
    rename_file("enabled")
    status_var.set("Mods Enabled")
    status_label.config(bg=MODS_ENABLED_COLOR)  # Red when mods are enabled

def disable_mods():
    rename_file("disabled")
    status_var.set("Play Vanilla")
    status_label.config(bg=VANILLA_COLOR)  # Bright green for vanilla

# Hide the console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Create buttons for "Mods Enabled", "Play Vanilla", and "Launch"
enable_button = tk.Button(root, text="Mods Enabled", command=enable_mods, width=15, height=2)
enable_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

disable_button = tk.Button(root, text="Play Vanilla", command=disable_mods, width=15, height=2)
disable_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Status label at the bottom left corner, styled to look like a button
status_label = tk.Label(root, textvariable=status_var, width=15, height=2, relief="solid", anchor="center", padx=10)
status_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Launch button at the bottom right
launch_button = tk.Button(root, text="Launch Balatro", command=launch_program, width=15, height=2)
launch_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Make the grid expand properly when resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Check status on startup
check_status()

# Run the Tkinter event loop
root.mainloop()
