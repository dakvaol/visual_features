import os
from pathlib import Path
#import tempfile
#import cv2
import numpy as np
#from colorthief import ColorThief
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import MiniBatchSparsePCA
from sklearn.cluster import KMeans
#from skimage.filters.rank import entropy
#from skimage.morphology import disk
#from PIL import Image, ImageStat
#from skimage import img_as_float
import pandas as pd
#from multiprocessing import Process
#import matplotlib.image as img
import matplotlib.pyplot as plt
import statistics
from scipy import spatial
#from numba import jit

#ratings = pd.read_csv('./ml-20m/ratings.csv')
#movie_list = pd.read_csv('movie_assets_sampled.csv')

# In case I do not have time to run the program
# The outputted features have been added to a CSV file 
movie_df = pd.read_csv('../datasets/output/output.csv')
shot_df = pd.read_csv('../datasets/output/shot_data.csv')


movie_df = movie_df.drop(columns=['Unnamed: 0', 'sharpness'])
shot_df = shot_df.drop(columns='Unnamed: 0')

#movie_df.head()