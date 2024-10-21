import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Set up logging
def setup_logger():
    logger = logging.getLogger("FolderRenamerLogger")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("folder_renamer.log")
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logger.addHandler(handler)
    return logger

class FolderRenamer(FileSystemEventHandler):
    def __init__(self, path, naming_scheme, logger):
        self.path = path
        self.naming_scheme = naming_scheme
        self.logger = logger

    def on_any_event(self, event):
        # Run the rename function only once
        self.rename_folders()
        observer.stop()  # Stop the observer after renaming

    def rename_folders(self):
        folders = [f for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]
        folder_counts = {}

        for folder in folders:
            count = sum([len(files) for r, d, files in os.walk(os.path.join(self.path, folder))])
            folder_counts[folder] = count

        sorted_folders = sorted(folder_counts.items(), key=lambda x: x[1], reverse=True)

        for i, (folder, _) in enumerate(sorted_folders, 1):
            old_path = os.path.join(self.path, folder)
            new_name = f"{i:02d}{self.naming_scheme}{folder}"
            new_path = os.path.join(self.path, new_name)

            if old_path != new_path:
                os.rename(old_path, new_path)
                self.logger.info(f"Renamed: {folder} -> {new_name}")
                print(f"Renamed: {folder} -> {new_name}")

def main():
    path = input("Enter the path to monitor: ")
    naming_scheme = input("Enter the naming scheme (e.g., '-' or '_'): ")

    # Setup logger
    logger = setup_logger()

    event_handler = FolderRenamer(path, naming_scheme, logger)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    # Run the observer only once for the first event
    observer.join()  # Wait for the first event

if __name__ == "__main__":
    main()
