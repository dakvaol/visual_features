from pathlib import Path
import shutil
import cv2
import numpy
import os
import re
from PIL import Image
import logging
import videokf as vf
from dotenv import load_dotenv

# Main extraction function
# Takes in the complete path to the video file being sampled 
def get_key_frames(path, keyframes_short): 
    vid_path = str(path)
    print(vid_path)
    path = Path(path)

    # Creates output folder for extracted keyframes
    if not os.path.exists(os.path.join(keyframes_short, vid_path[:-4])):
        os.makedirs(os.path.join(keyframes_short, vid_path[:-4]))

    # Deletes previous temporary keyframes directory if not previously deleted 
    #if(os.path.exists(os.path.dirname(path)+"keyframes")):
    #    shutil.rmtree(os.path.dirname(path)+"keyframes",
    #                  ignore_errors=False, onerror=None)
    # print("Keyframes are being extracted")

    # Using videokf library to extract i-frames
    vf.extract_keyframes(path, method="iframes")

    # Defines where the output of the extracted i-frames are
    folder = f'{os.path.dirname(path)}/keyframes'
    read = os.listdir(folder)
    read.sort(key=lambda f: int(re.sub('\D', '', f)))

    # Calculates absolute difference between extracted i-frames and adds them to output 
    # directory if they are over a given threshold
    for i in range(len(read)):
        try: 
            img1 = cv2.imread(os.path.join(folder, read[i-1]))
            img2 = cv2.imread(os.path.join(folder, read[i]))
            res = cv2.absdiff(img1, img2)
            res = res.astype(numpy.uint8)
            percentage = (numpy.count_nonzero(res) * 100) / res.size
            # This if sets the percentage absolute difference thershold
            if(percentage >= 75):
                shutil.move(os.path.join(
                    folder, read[i-1]), os.path.join(keyframes_short,vid_path[:-4], read[i-1]))
                print(read[i-1])
        except Exception:
            pass

    # Checking if temporary i-frames directory still exists
    if os.path.exists(folder):
        # Deletes the directory
        shutil.rmtree(folder)


if __name__== "__main__":
    movie_folder_path = Path("../movie_trailers")
    movie_read = os.listdir(movie_folder_path)

    ''' 
    logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
    '''
    for x in movie_read:
        try:
            vid_path = os.path.join(movie_folder_path, x)
            get_key_frames(vid_path)
        except Exception:
            logging.debug(f"Error getting keyframes from asset_id{x}")