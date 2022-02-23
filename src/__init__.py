#from i_frame import *
from scenedetection import *
from pathlib import Path
from i_frame import *
from features import *
from video_handler import *
import multiprocessing
import os

def initialize():
    movie_folder_path = Path("../movie_trailers")
    
    movie_read = os.listdir(movie_folder_path)
    
    for x in movie_read:
        vid_path = os.path.join(movie_folder_path, x)
        get_key_frames(vid_path)
        print('Keyframes extracted from movie: ', x)
    

    for x in movie_read:
        vid_path = os.path.join(movie_folder_path,x)
        movie_id = x #path.replace('./movie_keyframes/trailers/', '').replace('/','')
        feature_df = find_scenes(vid_path, movie_id)
        #scene_df = scene_df.append(feature_df)
        print('Shot length extracted from movie: ', x)
        feature_df.to_csv(f'../datasets/scene_output/{x[:-4]}.csv', index=False)
    
    
    
    keyframes = '../movie_keyframes/movie_trailers/'
    keyframes_read = os.listdir(keyframes)
    print(keyframes_read)


    for x in keyframes_read:
        #movie_df = pd.DataFrame()
        folder_path = os.path.join(keyframes,x)
        img_folder = os.listdir(folder_path)
        movie_id = x #path.replace('./movie_keyframes/trailers/', '').replace('/','')
        features = get_features(img_folder, movie_id, folder_path)
        #movie_df = movie_df.append(feature_dict)
        print('Features extracted from movie: ', x)
        features.to_csv(f'../datasets/movie_features/{x}.csv', index=False)

if __name__ == '__main__':
    initialize()
    
    #movie_df.head()
    