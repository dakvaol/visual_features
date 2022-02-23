from __future__ import print_function
import os
import pandas as pd
# Standard PySceneDetect imports:
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
# For caching detection metrics and saving/loading to a stats file
from scenedetect.stats_manager import StatsManager

# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector

scene_df = pd.DataFrame()

def find_scenes(video_path, movie_id):
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)

    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector())

    scene_list = []
    temp_df = pd.DataFrame(columns=['scene_nr', 'scene_timestamp', 'movie_id'])

    try:
        # Set downscale factor to improve processing speed.
        video_manager.set_downscale_factor()
        # Start video_manager.
        video_manager.start()
        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager)
        # Obtain list of detected scenes.
        scene_list = scene_manager.get_scene_list()
        # Each scene is a tuple of (start, end) FrameTimecodes.

        for i, scene in enumerate(scene_list):
            new_row = {
                'scene_nr': i, 
                'scene_timestamp': scene[0].get_seconds(),
                'movie_id': movie_id
                }
            temp_df = temp_df.append(new_row, ignore_index=True)
            i += 1
    finally:
        video_manager.release()

    return temp_df

# Main function to extract visual features from the movies
if __name__ == "__main__":
    trailers = './movie_trailers/'
    trailers_read = os.listdir(trailers)
    #print(trailers_read)
    
    for x in trailers_read:
        vid_path = os.path.join(trailers,x)
        
        movie_id = x #path.replace('./movie_keyframes/trailers/', '').replace('/','')
        feature_df = find_scenes(vid_path, movie_id)
        scene_df = scene_df.append(feature_df)
        print('Movie: ', x, ' done!')
    
    scene_df.to_csv('scene_data.csv')