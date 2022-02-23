import pandas as pd
import statistics as s

scene_df = pd.read_csv('../datasets/scene_output/scene_data.csv')
scene_df = scene_df.drop(columns='Unnamed: 0')
#scene_df = pd.read_csv('scene_data.csv')

# Averages a list
def average(l):
    return sum(l) / len(l)

# Makes a list of unique values from a list
def unique(list1):
    # Init null list
    unique_list = []

    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
            #print(x)
    return unique_list

# Gets the distance between 2 rows in a list
def mindistance(arr, N):
    return [arr[i] - arr[i-1] for i in range(1, N)]

def scene_matrix(scene_df, id):
    matrix = pd.DataFrame()
    temp = scene_df[scene_df['movie_id'] == id].copy()
    temp.reset_index(drop=True, inplace=True)
    
    N = len(temp['scene_timestamp'])
    shot_length = mindistance(temp['scene_timestamp'], N)

    shot_length = sorted(shot_length)
    
    average_shot_time = average(shot_length)
    mean_shot_time = s.median(shot_length)
    stdev_shot_time = s.stdev(shot_length)
    shots_per_second = temp['scene_nr'].iloc[-1] / temp['scene_timestamp'].iloc[-1]

    new_row = {
        'movie_id':id, 
        'shots_per_second': shots_per_second, 
        'mean_shot_time': mean_shot_time, 
        'average_shot_time': average_shot_time,
        'stdev_shot_time': stdev_shot_time}

    matrix = matrix.append(new_row, ignore_index = True)
    
    return matrix

if __name__ == '__main__':
    # Makes sure there is no overlap between movie_id's 
    unique_movie_id_list = unique(scene_df['movie_id'])
    print(unique_movie_id_list)

    shot_data = pd.DataFrame()

    for x in unique_movie_id_list:
        try:
            shot_data = shot_data.append(scene_matrix(scene_df, x))
        except:
            print(x,' is bein a bitch')
        print(x,' done!')
    
    shot_data.to_csv('shot_data.csv')