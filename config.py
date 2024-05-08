from pathlib import Path

home_folder = Path.home()

glob_locations = {
    "location_1": ("Downloads", str(Path.home() / "Downloads" / "*")),
    "location_2": ("ScanSnap Inbox", str(Path.home() / "Dropbox" / "Data Storage" / "ScanSnap Inbox" / "*")),
    "location_3": ("", ""),
    "location_4": ("", ""),
    "location_5": ("", ""),
    "location_6": ("", ""),
    "location_7": ("", ""),
    "location_8": ("", ""),
    "location_9": ("Other",""), # Folder Dialogue Do not use
}

