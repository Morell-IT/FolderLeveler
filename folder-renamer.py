import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderRenamer(FileSystemEventHandler):
    def __init__(self, path, naming_scheme):
        self.path = path
        self.naming_scheme = naming_scheme

    def on_any_event(self, event):
        self.rename_folders()

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
                print(f"Renamed: {folder} -> {new_name}")

def main():
    path = input("Enter the path to monitor: ")
    naming_scheme = input("Enter the naming scheme (e.g., '-' or '_'): ")

    event_handler = FolderRenamer(path, naming_scheme)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
