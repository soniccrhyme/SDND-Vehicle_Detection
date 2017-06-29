#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 08:53:10 2017

import images and pickle

@author: ucalegon
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import pickle
from skimage.util import img_as_ubyte
from skimage.color import rgb2hsv, rgb2luv, rgb2ycbcr
from skimage.exposure import rescale_intensity, equalize_adapthist
from tqdm import tqdm


### PARAMETERS ###

# If process_image, apply skimage.exposure.rescale_intensity & equalize_adapthist
process_image = False
# Color Map Choices: RGB, HSV, LUV, YCbCr
color_map = 'YCbCr'

def rgb_convert(img, color_map):
    
    
    if color_map == 'HSV':
        img_convert = rgb2hsv(img)
    elif color_map == 'LUV':
        img_convert = rgb2luv(img)
    elif color_map == 'YCbCr':
        img_convert = rgb2ycbcr(img)
    
    return img_convert


def import_images(process_image = False):
    print('Using {} color map'.format(color_map))
    print('Image Processing (rescale intensity & equalize_adapthist): {}'.format(process_image))
    
    
    vehicle_folders = ['GTI_Far', 'GTI_Right', 'GTI_Left', 'GTI_MiddleClose', 'KITTI_extracted']
    nonvehicle_folders = ['Extras', 'GTI']
    
    vehicles = []
    nonvehicles = []
    
    for folder in vehicle_folders:
        img_glob = glob.glob('clf_images/vehicles/{}/*.png'.format(folder))
        for img_file in tqdm(img_glob):
            img = img_as_ubyte(plt.imread(img_file))
            if process_image:
                img = img_as_ubyte(equalize_adapthist(rescale_intensity(img)))
            if color_map != 'RGB':
                assert color_map in ['HSV', 'LUV', 'YCbCr']
                img = rgb_convert(img, color_map)
            vehicles.append(img)
    print('{} Vehicle Images loaded into Numpy Array'.format(len(vehicles)))
    
    
    
    for folder in nonvehicle_folders:
        img_glob = glob.glob('clf_images/non-vehicles/{}/*.png'.format(folder))
        for img_file in tqdm(img_glob):
            img = img_as_ubyte(plt.imread(img_file))
            if process_image:
                img = img_as_ubyte(equalize_adapthist(rescale_intensity(img)))
            if color_map != 'RGB':
                assert color_map in ['HSV', 'LUV', 'YCbCr']
                img = rgb_convert(img, color_map)
            nonvehicles.append(img)
    print('{} Non-vehicle images loaded into Numpy Array'.format(len(nonvehicles)))
    
    
    all_vehicles = np.concatenate((vehicles, nonvehicles))
    vehicles_labels = np.ones(len(vehicles))
    nonvehicles_labels = np.zeros(len(nonvehicles))
    all_vehicles_labels = np.concatenate((vehicles_labels, nonvehicles_labels))
    
    if not process_image:
        with open('clf_images/all_vehicles_{}.pickle'.format(color_map), 'wb') as f:
            pickle.dump(all_vehicles, f)
        f.close()
        
        with open('clf_images/all_vehicles_labels.pickle', 'wb') as f:
            pickle.dump(all_vehicles_labels, f)
        f.close()
        print('Vehicle and Nonvehicle images and labels pickled as numpy array')
    else:
        with open('clf_images/all_vehicles_{}_processed.pickle'.format(color_map), 'wb') as f:
            pickle.dump(all_vehicles, f)
        f.close()
        
        with open('clf_images/all_vehicles_labels.pickle', 'wb') as f:
            pickle.dump(all_vehicles_labels, f)
        f.close()
        print('Vehicle and Nonvehicle processed images and labels pickled as numpy array')
        
    return
    
    

def main():
    
    
    import_images(process_image = process_image) 


if __name__ == '__main__':
    main()