import os
import sys
import time
from i_frame import *
from scenedetection import *
from features import *
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MonitorFolder(FileSystemEventHandler):

    #def __init__(self):
    #    super(MonitorFolder, self).__init__(patterns="*.mp4",
    #                                    # ignore_patterns=["*~"],
    #                                    ignore_directories=True, 
    #                                        case_sensitive=True)
    
    def on_created(self, event):
        print(event.src_path, event.event_type)
        #get_key_frames(event.src_path)
        print("Extracting key frames from: ", event.src_path)
         #self.checkFolderSize(event.src_path)
  
    def on_modified(self, event):
        print(event.src_path, event.event_type)
        #self.checkFolderSize(event.src_path)
'''    
             
    def checkFolderSize(self,src_path):
        if os.path.isdir(src_path):
            if os.path.getsize(src_path) >self.FILE_SIZE:
                print("Time to backup the dir")
            elif os.path.getsize(src_path) >self.FILE_SIZE:
                print("very big file")
'''

if __name__ == "__main__":
    src_path = Path('../movie_trailers/')

    event_handler=MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    print("Monitoring started")
    observer.start()
    try:
        while(True):
           time.sleep(1)
           
    except KeyboardInterrupt:
            observer.stop()
            observer.join()