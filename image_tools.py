#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 21:42:40 2020

@author: Gabe
"""

##image filtering tools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class im_pr:
    ##all fns will be written to expect and return int type
    def normalize_2d(img,bit_depth = 8):
        ##normalize 2d / greyscale image
        
        ## Set lower bound to zero
        
        min_val_img = np.min(np.min(img))
        new_img = img - min_val_img
        new_img = new_img.astype(float)
        
        ## Scale so upper bound is 2**bit depth, assuming default of 8-bit
        max_val_bd = 2.0 ** bit_depth
        max_val_img = float(np.max(np.max(new_img)))
        new_img *= (max_val_bd/max_val_img)
        new_img = new_img.astype(int)
        
        return new_img
    
    def make_bw(img):
        img = np.mean(img,axis=2)
        return img.astype(int)
    
    def edge_pad(img, extra_border, method = "zero_pad"):
        if(method == "zero_pad"):
            img_dims = img.shape
            new_img = np.zeros([img_dims[0]+2*extra_border, img_dims[1]+2*extra_border], dtype=float)

        # if(method == "mirror"):
        #     new_img = np.zeros([img_dims[0]+2*extra_border, img_dims[1]+2*extra_border], dtype=float)

        new_img[extra_border:-extra_border,extra_border:-extra_border] = img  
            
        return new_img.astype(int)
        
    
    def apply_filter(img,filt,edge_method = "zero_pad"):
        
        fheight,fwidth = filt.shape  ##filter should be symmetric
        if(fheight%2 == 0 | fwidth%2 == 0):   
            print("WARNING: Filter should have odd dimensions\n\n") ##needs odd side lengths to act symmetrically on a pixel
            return -1
        extra_border = int((np.shape(filt)[0] - 1) / 2) ##this is the extra border pixels for filter - will be added to all sides of image

        height,width = img.shape
        nimg = im_pr.normalize_2d(img)
        padded_img = im_pr.edge_pad(nimg, extra_border)
        
        filtered_padded_img = np.empty_like(img,dtype=float)
        
        for row in range(extra_border,extra_border + height):
            yrange = [row - extra_border, row + extra_border + 1]
            og_row = row-extra_border
            for col in range(extra_border, extra_border + width):
                xrange = [col - extra_border, col + extra_border + 1]
                og_col = col-extra_border
                
                filtered_padded_img[og_row,og_col] = np.sum(np.sum(filt*padded_img[yrange[0]:yrange[1],xrange[0]:xrange[1]]))
        
        filtered_padded_img = im_pr.normalize_2d(filtered_padded_img)
    
        return filtered_padded_img
    
    
        ##new image should have same dimensions plus 2*extra_border in each direction
                
        
            
            
            
            
            
            
            
    