import os
import cv2
import numpy as np
from colorthief import ColorThief
from skimage.filters.rank import entropy
from skimage.morphology import disk
import pandas as pd

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

# Calculates brightness by splitting HSV color space into 
# hue, saturation, and value. The value is synonymous with brightness.
def get_brightness(img):
    image = img.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #cv2.imshow('Image', hsv)
    _, _, v = cv2.split(hsv)
    sum = np.sum(v, dtype=np.float32)
    num_of_pixels = v.shape[0] * v.shape[1]
    return (sum * 100.0) / (num_of_pixels * 255.0)

# Calculates saturation by splitting HSV color space into 
# hue, saturation, and value. Saturation is extracted and represents
# saturation
def get_saturation(img):
    image = img.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #cv2.imshow('Image', hsv)
    _, s, _ = cv2.split(hsv)
    sum = np.sum(s, dtype = np.float32)
    num_of_pixels = s.shape[0] * s.shape[1]
    return (sum * 100.0) / (num_of_pixels * 255.0)

# Calculates entropy
def get_entropy(img):
    image = img.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    entropy_img = entropy(gray,disk(5))
    all_sum = np.sum(entropy_img, dtype = np.float32)
    num_of_pixels = entropy_img.shape[0] * entropy_img.shape[1]
    return all_sum / num_of_pixels

# Calculates image sharpness by the variance of the Laplacian
def get_sharpness(img):
    image = img.copy()
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(img2gray, cv2.CV_64F).var()

# Return contrast (RMS contrast)
def get_contrast(img):
    image = img.copy()
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return img_gray.std()

def get_colorfulness(img):
    image = img.copy()
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))
    # compute rg = R - G
    rg = np.absolute(R - G)
    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)
    # compute the mean and standard deviation of both `rg` and `yb`
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    # combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    # derive the "saturation" metric and return it
    return stdRoot + (0.3 * meanRoot)

# Returns color palette of a frame as a set
def get_palette(filename):
    color_thief = ColorThief(filename)
    return color_thief.get_palette(color_count=5)

# Adds values for each picture to a list so they can be later averaged and 
# made into a dataframe. 
def get_features(image_folder, movie_id, folder_path):
    movie_dict = {}
    df = pd.DataFrame()
    saturation_list = []
    brightness_list = []
    entropy_list = []
    sharpness_list = []
    contrast_list = []
    colorfulness_list = []
    dominant_color_list = []
    frame_list = []

    for i in range(len(image_folder)):
        try:
            img = cv2.imread(os.path.join(folder_path, image_folder[i]))
            frame_brightness = get_brightness(img)
            frame_saturation = get_saturation(img)
            frame_entropy = get_entropy(img)
            frame_sharpness = get_sharpness(img)
            frame_contrast = get_contrast(img)
            frame_colorfulness = get_colorfulness(img)
            frame_domcolor = get_palette(os.path.join(folder_path, image_folder[i]))

            saturation_list.append(frame_saturation)
            brightness_list.append(frame_brightness)
            entropy_list.append(frame_entropy)
            sharpness_list.append(frame_sharpness)
            contrast_list.append(frame_contrast)
            colorfulness_list.append(frame_colorfulness)
            dominant_color_list.append(frame_domcolor)
            frame_list.append(image_folder[i][:-4])
        except Exception:
            print("Failure at frame_nr:", i)

    # Create movie dictionary
    movie_dict = {
            'saturation': saturation_list,
            'brightness': brightness_list, 
            'entropy': entropy_list, 
            'sharpness': sharpness_list, 
            'contrast': contrast_list,
            'frame_nr': frame_list,
            'colorfulness': colorfulness_list,
            'col_palette': dominant_color_list,
            'movie_id': movie_id
            }

    df = pd.DataFrame(movie_dict)
    df['frame_nr'] = pd.to_numeric(df['frame_nr'], downcast='integer')
    df = df.sort_values(by = ['frame_nr', 'movie_id'], ascending=[True, True])
    print(movie_id, " done")
    return df

if __name__ == "__main__":
    movie_df = pd.DataFrame()
    trailers = '../movie_keyframes/movie_trailers/'
    trailers_read = os.listdir(trailers)
    #print(trailers_read)
    
    for x in trailers_read:
        folder_path = os.path.join(trailers,x)
        img_folder = os.listdir(folder_path)
        
        movie_id = x #path.replace('./movie_keyframes/trailers/', '').replace('/','')
        feature_dict = get_features(img_folder, movie_id)
        movie_df = movie_df.append(feature_dict)
        print(x, " competed!")
    
    movie_df.head()
    movie_df.to_csv('movie_df.csv', index=False)