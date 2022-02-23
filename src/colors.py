import pandas as pd
from scipy.spatial import KDTree
from itertools import chain
from collections import Counter
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)

color_names = pd.read_csv('../datasets/color_names/colornames.csv')
color_names_dict = color_names.to_dict()
df = pd.read_csv("../datasets/output.csv")
#df.head()

# Makes a list of unique values from a list
def unique(list1):
    # Init null list
    unique_list = []

    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
            #print(x)
    return unique_list

def strip_colors():
    col_df = df.copy()
    col_df = col_df.replace('\[','', regex=True)
    col_df = col_df.replace('\]','', regex=True)

    col_df = col_df.replace('\),',').', regex=True)

    print(col_df['col_palette'])

    col_df[['dom_col1', 'dom_col2', 'dom_col3', 'dom_col4', 'dom_col5']] = col_df['col_palette'].str.split('.',0,expand=True)
    col_df = col_df.drop(columns=['Unnamed: 0', 'saturation', 'brightness', 'entropy', 'sharpness', 'contrast', 'frame_nr', 'colorfulness'])
    unique_movie_id_list = unique(col_df['movie_id'])
    col_df.head()
    return unique_movie_id_list, col_df

def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []    
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)    
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

#print(convert_rgb_to_names((255,1,2)))

def pool_colors(df, id):
    col1 = df['dom_col1'][df['movie_id'] == id]
    col2 = df['dom_col2'][df['movie_id'] == id]
    col3 = df['dom_col3'][df['movie_id'] == id]
    col4 = df['dom_col4'][df['movie_id'] == id]
    col5 = df['dom_col5'][df['movie_id'] == id]

    return list(chain(col1, col2, col3, col4, col5))

def get_most_common_color(unique_list, col_df, number_of_results):
    for x in unique_list:
        col_pool = pool_colors(col_df, x)
        c = Counter(col_pool)
        print("Element with highest frequency:\n",c.most_common(5))
    #print(col_pool)
    return c.most_common(number_of_results)