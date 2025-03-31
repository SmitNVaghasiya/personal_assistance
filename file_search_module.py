import os
import platform
import string

def get_available_drives():
    """
    Returns a list of available drives on the system (e.g., ['C:\\', 'D:\\'] on Windows).
    """
    if platform.system() != "Windows":
        # For non-Windows, start from root
        return ["/"]
    
    drives = []
    for drive_letter in string.ascii_uppercase:
        drive = f"{drive_letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def search_and_open_file(filename):
    """
    Searches for a file across all drives and opens it if found.
    Matches filenames even if the extension is not provided.
    Returns a message indicating success or failure.
    """
    print("Search started...")
    
    # Get all available drives
    search_roots = get_available_drives()
    found_file = None

    # Clean the filename (remove extra spaces, convert to lowercase for comparison)
    search_name = filename.strip().lower()
    # Split the search name to handle cases where user might include extension
    search_base, _ = os.path.splitext(search_name)

    # Search through each drive
    for root in search_roots:
        try:
            for dirpath, _, files in os.walk(root):
                for file in files:
                    # Get the base name of the file (without extension) for comparison
                    file_base, _ = os.path.splitext(file)
                    if file_base.lower() == search_base or file.lower() == search_name:
                        found_file = os.path.join(dirpath, file)
                        break
                if found_file:
                    break
        except (PermissionError, OSError):
            # Skip directories we don't have permission to access
            continue
        if found_file:
            break

    if found_file:
        try:
            # Open the file using the default application
            if platform.system() == "Windows":
                os.startfile(found_file)  # Windows-specific
            else:
                # For macOS or Linux, use 'open' or 'xdg-open'
                os.system(f"open {found_file}" if platform.system() == "Darwin" else f"xdg-open {found_file}")
            return f"Opening {os.path.basename(found_file)} at {found_file}."
        except Exception as e:
            return f"Error opening {os.path.basename(found_file)}: {e}"
    else:
        return f"Could not find {filename} on your system."