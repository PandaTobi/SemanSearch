import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import search_file
import os

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            search_file.index_files(os.path.dirname(event.src_path))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Directory to check for new files")

    args = parser.parse_args()

    if args.path:
        path_to_watch=args.path
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path=path_to_watch, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()