from scenedetection import *
from pathlib import Path
from i_frame import *
from features import *
from video_handler import *
from shot_metrics import *
from combining_data import * 
import logging
import os
from dotenv import load_dotenv

# Function starting starting the other scripts in succession
def initialize( 
    delete_trailers: bool,
    trailer_path, 
    keyframe_path, 
    keyframes_short, 
    scene_output, 
    feature_output,
    shot_csv_path,
    shot_data_output,
    raw_output,
    final_output
    ):
    movie_folder_path = Path(trailer_path)
    movie_read = os.listdir(movie_folder_path)

    for x in movie_read:
        vid_path = os.path.join(movie_folder_path, x)
        get_key_frames(vid_path, keyframes_short)
    logging.info("Keyframes successfully extracted")

    for x in movie_read:
        vid_path = os.path.join(movie_folder_path,x)
        movie_id = x 
        scene_df = find_scenes(vid_path, movie_id)
        filename = f'{scene_output}{x[:-4]}.csv'
        filename = filename.replace('"', "")
        scene_df.to_csv(filename, index=False)
    logging.info("Scene data successfully extracted")

    keyframes = keyframe_path
    keyframes_read = os.listdir(keyframes)

    for x in keyframes_read:
        #movie_df = pd.DataFrame()
        folder_path = os.path.join(keyframes,x)
        img_folder = os.listdir(folder_path)
        movie_id = x #path.replace('./movie_keyframes/trailers/', '').replace('/','')
        features = get_features(img_folder, movie_id, folder_path)
        #movie_df = movie_df.append(feature_dict)
        #print('Features extracted from movie: ', x)
        features.to_csv(f'{feature_output}{x}.csv', index=False)

    logging.info("Features successfully extracted")

    shot_csv_path = Path(shot_csv_path)
    shot_csv = os.listdir(shot_csv_path)
    list_of_shots = [pd.read_csv(os.path.join(shot_csv_path,csv)) for csv in shot_csv]
    scene_df = pd.concat(list_of_shots)

    # Makes sure there is no overlap between movie_id's 
    unique_movie_id_list = unique(scene_df['movie_id'])
    print(unique_movie_id_list)

    shot_data = pd.DataFrame()

    for x in unique_movie_id_list:
        try:
            shot_data = shot_data.append(scene_matrix(x, shot_csv_path))
        except Exception:
            logging.debug(f'AssetID {x} is throwing excpetions when calculating shot metrics')

    shot_data.to_csv(shot_data_output, index=False)
    logging.info("Shots condenced")

    combine_data(feature_output, shot_data_output, raw_output, final_output)
    print(f'Final featurelist successfully outputted to dir {final_output}')

    if delete_trailers:
        completed_trailers = pd.read_csv(final_output)
        trailer_list = list(completed_trailers['movie_id'].unique())

        for filename in trailer_list:
            # Checking if temporary i-frames directory still exists
            if os.path.exists(os.path.join(trailer_path, str(filename), '.mp4')):
                # Deletes the directory
                shutil.rmtree(os.path.join(str(filename), '.mp4'))
        

if __name__ == '__main__':
    env_var = load_dotenv('.env')
    trailer_path = os.getenv('TRAILERS')
    keyframes_path = os.getenv('KEYFRAMES')
    keyframes_short = os.getenv('KEYFRAMES_SHORT')
    feature_path = os.getenv('MOVIE_FEATURES')
    scene_output = os.getenv('SCENE_OUTPUT')
    shot_csv_path = os.getenv('SCENE_OUTPUT')
    shot_data = os.getenv('SHOT_DATA')
    raw_output = os.getenv('RAW_FEATURES')
    final_output = os.getenv('FINAL_OUTPUT')

    initialize( 
        True,
        trailer_path, 
        keyframes_path, 
        keyframes_short, 
        scene_output, 
        feature_path, 
        shot_csv_path, 
        shot_data,
        raw_output,
        final_output
        )
    