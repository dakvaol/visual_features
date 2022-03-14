import os
from pathlib import Path
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from scipy import spatial
from dotenv import load_dotenv

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

# Polynomial regression on the features related to the mobies
def polynomial_regression_alt(df, id):
    temp_df = df
    temp_df['frame_nr'] = pd.to_numeric(temp_df['frame_nr'], downcast='integer')
    temp_df = temp_df.sort_values(by=['frame_nr'], axis=0, ascending=True)
    output = pd.DataFrame()

    frame_nr = temp_df['frame_nr'][temp_df['movie_id'] == id]
    saturation = temp_df['saturation'][temp_df['movie_id'] == id]
    brightness = temp_df['brightness'][temp_df['movie_id'] == id]
    entropy = temp_df['entropy'][temp_df['movie_id'] == id]
    #sharpness = temp_df['sharpness'][temp_df['movie_id'] == id]
    contrast = temp_df['contrast'][temp_df['movie_id'] == id]
    colorfulness = temp_df['colorfulness'][temp_df['movie_id'] == id]

    saturation_model_1st = np.poly1d(np.polyfit(frame_nr, saturation, 1))
    brightness_model_1st = np.poly1d(np.polyfit(frame_nr, brightness, 1))
    entropy_model_1st = np.poly1d(np.polyfit(frame_nr, entropy, 1))
    #sharpness_model_1st = str(np.poly1d(np.polyfit(frame_nr, sharpness, 1)))
    contrast_model_1st = np.poly1d(np.polyfit(frame_nr, contrast, 1))
    colorfulness_model_1st = np.poly1d(np.polyfit(frame_nr, colorfulness, 1))

    saturation_model_2nd = np.poly1d(np.polyfit(frame_nr, saturation, 2))
    brightness_model_2nd = np.poly1d(np.polyfit(frame_nr, brightness, 2))
    entropy_model_2nd = np.poly1d(np.polyfit(frame_nr, entropy, 2))
    #sharpness_model_2nd = str(np.poly1d(np.polyfit(frame_nr, sharpness, 2)))
    contrast_model_2nd = np.poly1d(np.polyfit(frame_nr, contrast, 2))
    colorfulness_model_2nd = np.poly1d(np.polyfit(frame_nr, colorfulness, 2))

    polynomial_dict = {
        'movie_id': id,
        'saturation_model_1st': saturation_model_1st, 
        'brightness_model_1st': brightness_model_1st,
        'entropy_model_1st': entropy_model_1st,
        #'sharpness_model_1st': sharpness_model_1st,
        'contrast_model_1st': contrast_model_1st,
        'colorfulness_model_1st': colorfulness_model_1st,
        'saturation_model_2nd': saturation_model_2nd,
        'brightness_model_2nd': brightness_model_2nd,
        'entropy_model_2nd': entropy_model_2nd,
        #'sharpness_model_2nd': sharpness_model_2nd,
        'contrast_model_2nd': contrast_model_2nd,
        'colorfulness_model_2nd': colorfulness_model_2nd,
    }

    output = output.append(polynomial_dict, ignore_index=True)
    return output

# New dataframe condensing each movie into a single row 
def movie_matrix(df, id):
    matrix = pd.DataFrame()

    avg_brightness = average(df['brightness'][df['movie_id'] == id])
    avg_saturation = average(df['saturation'][df['movie_id'] == id])
    avg_entropy = average(df['entropy'][df['movie_id'] == id])
    #avg_sharpness = average(df['sharpness'][df['movie_id'] == id])
    avg_contrast = average(df['contrast'][df['movie_id'] == id])
    avg_colorfulness = average(df['colorfulness'][df['movie_id'] == id])

    stdev_brightness = statistics.stdev((df['brightness'][df['movie_id'] == id]))
    stdev_saturation = statistics.stdev((df['saturation'][df['movie_id'] == id]))
    stdev_entropy = statistics.stdev((df['entropy'][df['movie_id'] == id]))
    #stdev_sharpness = statistics.stdev((df['sharpness'][df['movie_id'] == id]))
    stdev_contrast = statistics.stdev((df['contrast'][df['movie_id'] == id]))
    stdev_colorfulness = statistics.stdev((df['colorfulness'][df['movie_id'] == id]))

    mean_brightness = statistics.median((df['brightness'][df['movie_id'] == id]))
    mean_saturation = statistics.median((df['saturation'][df['movie_id'] == id]))
    mean_entropy = statistics.median((df['entropy'][df['movie_id'] == id]))
    #mean_sharpness = statistics.median((df['sharpness'][df['movie_id'] == id]))
    mean_contrast = statistics.median((df['contrast'][df['movie_id'] == id]))
    mean_colorfulness = statistics.median((df['colorfulness'][df['movie_id'] == id]))

    matrix_dict = {
        'movie_id': id,
        'avg_brightness': avg_brightness,
        'avg_saturation': avg_saturation,
        'avg_entropy': avg_entropy,
        #'avg_sharpness': avg_sharpness,
        'avg_contrast': avg_contrast,
        'avg_colorfulness': avg_colorfulness,
        'stdev_brightness': stdev_brightness,
        'stdev_saturation': stdev_saturation,
        'stdev_entropy': stdev_entropy,
        #'stdev_sharpness': stdev_sharpness,
        'stdev_contrast': stdev_contrast,
        'stdev_colorfulness': stdev_colorfulness,
        'mean_brightness': mean_brightness,
        'mean_saturation': mean_saturation,
        'mean_entropy': mean_entropy,
        #'mean_sharpness': mean_sharpness,
        'mean_contrast': mean_contrast,
        'mean_colorfulness': mean_colorfulness,
    }

    matrix = matrix.append(matrix_dict, ignore_index = True)
    return matrix

# Cosine similarity between two rows
def compute_cos_sim(array1, array2):
    return 1 - spatial.distance.cosine(array1, array2)

# Cosine similarity between all rows
def compute_cos_sim_all(my_array):
    n_rows = my_array.shape[0]
    cos_sim_array = np.zeros((n_rows,n_rows))
    for row1 in range(n_rows):
        for row2 in range(n_rows):
            cos_sim_array[row1,row2] = \
            compute_cos_sim(my_array[row1, :],\
                            my_array[row2, :])
    return cos_sim_array

# Combines shot data with visualfeatures
def combine_data(feature_path, shot_data , raw_output, pre_norm_output, final_output):
    features_csv_path = Path(feature_path)
    feature_csv = os.listdir(features_csv_path)
    list_of_features = [pd.read_csv(os.path.join(features_csv_path, csv)) for csv in feature_csv]


    movie_df = pd.concat(list_of_features)
    shot_df = pd.read_csv(shot_data)

    unique_movie_id_list = unique(movie_df['movie_id'])

    # Makes two dataframes
    # One containing polynomials, and one containing averages etc. 
    poly_df = pd.DataFrame()
    matrix_df = pd.DataFrame()

    for x in unique_movie_id_list:
        poly_df = poly_df.append(polynomial_regression_alt(movie_df, x))
        matrix_df = matrix_df.append(movie_matrix(movie_df, x))
        
    #poly_df = poly_df.astype(str) 
    final_matrix = pd.merge(poly_df, matrix_df, on = 'movie_id')
    final_matrix.to_csv(raw_output, index=False)
    final_df = pd.merge(shot_df, final_matrix, on = 'movie_id')
    no_poly_df = pd.merge(shot_df, matrix_df, on = 'movie_id')

    movie_minmax = no_poly_df.copy()
    extracted_col = no_poly_df[["movie_id"]]
    movie_minmax = movie_minmax.drop(columns = (["movie_id"]))
    columns = movie_minmax.columns

    #scaler = StandardScaler()
    minmax = MinMaxScaler()
    # Standarization
    #movie_standard = scaler.fit_transform(movie_minmax)
    movie_minmax.to_csv(pre_norm_output, index=False)
    movie_minmax = minmax.fit_transform(movie_minmax)

    mdf = pd.DataFrame(movie_minmax, columns=columns)
    mdf = mdf.join(extracted_col)
    mdf.to_csv(final_output, index=False)

    #cos_sim_values = compute_cos_sim_all(movie_minmax)
    #cos_df = pd.DataFrame(cos_sim_values)
    #cos_df.to_csv('cos_sim_values.csv')

if __name__ == "__main__":
    env_var = load_dotenv('.env')
    feature_path = os.getenv('MOVIE_FEATURES')
    shot_data = os.getenv('SHOT_DATA')
    raw_output = os.getenv('RAW_FEATURES')
    pre_norm_output = os.getenv('PRE_NORM_OUTPUT')
    final_output = os.getenv('FINAL_OUTPUT')
    combine_data(feature_path ,shot_data ,raw_output,pre_norm_output , final_output)
