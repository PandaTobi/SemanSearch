import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import search_file
import os

## Currently the watchdog observer watches the correct path (I think), but the search_file module
## is not set up to handle the path argument correctly.

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"\n\nNew file detected: {event.src_path}")
            search_file.index_files(os.path.dirname(event.src_path))

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"\n\nFile deleted: {event.src_path}")
            search_file.index_files(os.path.dirname(event.src_path))

if __name__ == "__main__":
    import argparse
    import search_file
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Directory to check for new files")

    args = parser.parse_args()
 
    if args.path:
        search_file.index_files(args.path)

        path_to_watch=args.path
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path=path_to_watch, recursive=True)
        observer.start()

        try:
            while True:
                query = input("Enter a search query (or nothing to quit): ")
                if query.strip() == '':
                    observer.stop()
                    break
                matches = search_file.semantic_search(query)
                for match in matches:
                    print(match)
                print("Search complete.\n")
        except KeyboardInterrupt:
            observer.stop()
        observer.join()