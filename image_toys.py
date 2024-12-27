#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 19:38:00 2019

@author: Gabe
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt

######################################################################################
def take_names_jpg(path):
    file_list = []
    jpg_re = re.compile("\w+(.jpg)", re.IGNORECASE)
    if os.path.isdir(path):
        for elem in os.listdir(path):
            jpg_match = jpg_re.match(elem)
            if(jpg_match):
                file_list.append(elem)
    return file_list

######################################################################################

def make_square(full_array):
    ##takes 3d image, passes out square image center-cropped
    flat_array = full_array[:,:,0]
    dims = list(np.shape(flat_array))
    short_side = np.min(dims)
    long_side = np.max(dims)

    long_side_new_start = int(long_side/2 - short_side/2)
    new_long_axis = [long_side_new_start, long_side_new_start + short_side]
    if short_side == dims[0]:
        full_array = full_array[:,new_long_axis[0]:new_long_axis[1],:]
    else:
        full_array = full_array[new_long_axis[0]:new_long_axis[1],:,:]
        
    return full_array
 
######################################################################################    

def catalog_all_images(path):
    ##goes through images, computes r/g/b values for each and returns them as a dict like this -> {filename:[r_val,g_val,b_val]}
    color_dict = {}
    if os.path.isdir(path):
        file_list = take_names_jpg(path)
    else:
        print("Invalid path name for fn catalog_all_images: {}".format(path))
  
    for elem in file_list:
        full_path = path + "//" + elem
        img = plt.imread(full_path)
        ##Send out image to make_square fn
        
        img = make_square(img)
        color_list = []
        for color_ct in range(3):
            color_list.append(np.mean(img[:,:,color_ct]))
        color_dict[elem] = color_list
        
    return color_dict

######################################################################################

def pixelate_img(img, new_x_dim, new_y_dim, is_square = 0):
    #pixelate square image from n x n to new_dim x new_dim 
    if(is_square):
        img = make_square(img)
        
    new_img = np.empty([new_y_dim,new_x_dim,3],dtype="uint8")
    x_inc = np.shape(img)[1] / float(new_x_dim)
    y_inc = np.shape(img)[0] / float(new_y_dim)
    
    for xct in range(new_x_dim):
        x_chunk = [x_inc * xct, x_inc * (xct + 1)]
        x_inds = [int(np.floor(x_chunk[0])), int(np.floor(x_chunk[1]))]

        for yct in range(new_y_dim):
            y_chunk = [y_inc * yct, y_inc * (yct + 1)]
            y_inds = [int(np.floor(y_chunk[0])), int(np.floor(y_chunk[1]))]

            for color in range(3):
                new_img[yct,xct,color] = round(np.mean(img[y_inds[0]:y_inds[1],x_inds[0]:x_inds[1],color]))

    return new_img
######################################################################################

def save_square_pixelated_images(read_path, chunk_dim):
    save_path = read_path + "//{}_pixel_squares".format(chunk_dim)
    
    if os.path.isdir(save_path):
        return save_path
    else:
        os.mkdir(save_path)
        file_list = take_names_jpg(read_path)
        for elem in file_list:
            imread_path = read_path + "//{}".format(elem)
            img = plt.imread(imread_path)
            img = pixelate_img(img, chunk_dim, chunk_dim, is_square = 1)
            plt.imsave(save_path + "//{}".format(elem), img)
        return save_path

######################################################################################

def chunkify_img(img,library_path,color_dict,chunk_dim):
    #take image, pixelate it to desired dimension, pixelate(make_square(image library)) to same dimension so images can fit in same size as original image, find correct images to replace each chunk
    orig_size = np.array(np.shape(img[:,:,0]))
    final_size = orig_size - orig_size % chunk_dim
    final_size = np.array([int(final_size[0]),int(final_size[1]),3])
    final_img = np.empty(final_size, dtype = "uint8")    
    square_im_path = save_square_pixelated_images(library_path, chunk_dim)
    
    for y_ind in range(int(final_size[0] / chunk_dim)):
        yrange = [y_ind * chunk_dim, (y_ind+1) * chunk_dim]

        for x_ind in range(int(final_size[1] / chunk_dim)):
            xrange = [x_ind * chunk_dim, (x_ind+1) * chunk_dim]

            color_list = []             
            max_error = 1000
            for color in range(3):
                color_list.append(np.mean(img[yrange[0]:yrange[1],xrange[0]:xrange[1],color]))   
            for key in color_dict:
                error = np.mean(np.abs(np.array(color_dict[key]) - np.array(color_list)))
                if error < max_error:
                    max_error = error
                    best_key = key
            chosen_im = plt.imread(square_im_path + "//{}".format(best_key))
            final_img[yrange[0]:yrange[1],xrange[0]:xrange[1],:] = chosen_im
        
    return final_img

######################################################################################

if __name__ == "__main__":
    
    library_path = r"/Users/Gabe/Pictures/instagram_images"            ##Make this one the path to your photo library
#    photo_path = r"/Users/Gabe/Desktop/wallpapers/DSC_0022.jpg"              ##Make this one the path to the photo you want collagified
    chunk_dim = 40                ##This value determines the size of the "pixels" in the collage
                                  ##Default value of 50 -> each square of 50x50 pixels will be 
                                  ##replaced with the closest image from your library
#    save_name = r"collage"        ##Save name is the name that the collage will be saved to inside of your library_path

    ######################################################################################
    ## Don't touch below here unless you are l33t sup3r h4x0r 
    ######################################################################################
    color_dict = catalog_all_images(library_path)
    file_list = take_names_jpg(library_path)
    pix_dir = library_path + "//{}_pixels_pixelated_library".format(chunk_dim)
    os.mkdir(pix_dir)

    for elem in file_list:
        img = plt.imread(library_path + "//{}".format(elem))
        collage = chunkify_img(img,library_path,color_dict,chunk_dim)

        plt.imsave(pix_dir + "//{}".format(elem), collage, format="jpg")
#    plt.imshow(collage)
#    plt.show()     
        
        