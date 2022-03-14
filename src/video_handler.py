import os
import pandas as pd 
import json
import requests
from pathlib import Path
from i_frame import * 
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv


# Makes a list of unique assets from a series of assets
def get_assets(series):
    unique_list = []
    for x in series:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

# Get a specific title based on the movie title 
def get_asset(title: str, df, asset_col, title_col):
    return df[asset_col].loc[df[title_col] == title] 

# Gets url that is used to retrieve JSON object containing uri's 
def get_url(asset_id: str, url: str, url_end: str):
    return url+asset_id+url_end

# Gets uri to download 
def get_uri(url: str, auth: str, rate):
    headers = CaseInsensitiveDict()
    headers['Authorization'] = auth
    r = requests.get(url, headers=headers)
    js = r.json()
    uri_bitrate = next((item for item in js if item["bitrate"] == rate), None)
    return uri_bitrate['uri']

# Uses shell commands to download video
#def get_video_alt(asset): #):
#   URL = f"https://progressive-tv2-no.akamaized.net/ismusp/isi_mp4_1/{asset}.mp4"
#   URL = "https://progressive-tv2-no.akamaized.net/ismusp/isi_mp4_1/2021-10-14/CM_JOKER_210828_clean_Sc\(1692663_R222MP41000\).mp4"
#   subprocess.call(f"youtube-dl {URL} -o '../movie_trailers/{asset}.mp4'", shell = True, executable = "/bin/zsh")

# Uses request library to download videofiles 
def get_video(filename, uri):
    filename = f'{filename}.mp4'
    r = requests.get(uri)
    f = open(f'../movie_trailers/{filename}', 'wb')
    for chunk in r.iter_content(chunk_size=255):
        if chunk:
            f.write(chunk)
    f.close

# Downloads all trailers in a batch
def batch_downloads(df, url: str, url_end: str, auth: str, rate):
    asset_ids = get_assets(df['promoAssetId'])
     
    for asset_id in asset_ids:
        try: 
            filename = df['assetId'][df['promoAssetId'] == asset_id]
            filename = filename.iloc[0]
            compl_url = get_url(str(asset_id), url, url_end)
            uri = get_uri(compl_url, auth, rate)
            logging.debug('URI gathred')
            get_video(filename, uri)
        except Exception:
            logging.debug(f'Failure with downloading movie with asset id {filename}')
    

if __name__ == "__main__":
    #df = pd.read_csv('../datasets/movie_assets/movie_assets_exposed.csv')
    #assets = get_assets(df['assetId'])
    env_var = load_dotenv('.env')
    movie_path = os.getenv('TRAILERS')
    movie_assets = os.getenv('MOVIE_ASSETS')

    print(movie_path)

     
    movie_dir = Path(movie_path)
    df = pd.read_csv(movie_assets)
    url = os.getenv('URL')
    url_end = os.getenv('URL_end')
    auth = os.getenv('AUTH')
    bitrate = 1000
    batch_downloads(df, url, url_end, auth, bitrate)


    #url = get_url('1692663', os.getenv('URL'), os.getenv('URL_end'))
    #uri = get_uri(url, os.getenv('AUTH'), 1000)
    #get_video('joker', uri)
    
    
    #movie_folder_path = movie_dir
    
    movie_read = os.listdir(movie_dir)
    
    for x in movie_read:
        try: 
            vid_path = os.path.join(movie_folder_path, x)
            get_key_frames(vid_path)
            logging.debug(f'Keyframes successfully extracted from movie: {x}')
        except Exception:
            logging.debug(f"Invalid filetype for trailer {x}")
    