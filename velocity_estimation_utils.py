#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
velocity_estimation_utils.py

"""

import numpy as np
import imageio

def GaussianKernel2D(kernel_size, sigma):
    '''Returns a 2D Gaussian kernel
    
    kernel_size: Gaussian kernel size
    sigma: kernel standard deviation
    '''
    
    kn = int((kernel_size - 1) / 2);
    x = np.arange(-kn, kn + 1, 1);
    [X, Y] = np.meshgrid(x, x, sparse=False, indexing='xy');
    kernel = np.exp(-(np.power(X, 2) + np.power(Y, 2)) / (2 * sigma ** 2));
    kernel = kernel / kernel.sum();
    return kernel;

def MakeMovie(image, nf, space_ship, x_start, y_start, x_vel, y_vel):
    '''Returns a simulated video with the moving object superimposed on the image
    
    nf: number of frames
    space_ship: a tupil of (Gaussian kernel size, kernel standard deviation)
    x_start: x starting position of moving object
    y_start: y starting position of moving object
    x_vel: x component velocity of object (pixels / frame)
    y_vel: y component velocity of object (pixels / frame)
    '''   
    
    [nr, nc] = image.shape;
    space_ship_size = space_ship[0];
    ship = GaussianKernel2D(space_ship[0], space_ship[1]);
    video = np.zeros((nf, nr, nc));
    for frame_no in range(nf):   
        video[frame_no, :, :] = image;
    
    for frame_no in range(nf):   
        video[frame_no, y_start: y_start + space_ship_size, x_start: x_start + space_ship_size] = ship;        
        x_start += x_vel;
        y_start += y_vel;
        if x_start >= (nc - space_ship_size) or y_start >= (nr - space_ship_size):
            break;           

    mask = video < 0;
    video[mask] = 0;            
    return video;

def SaveMovie(movie, movie_name, fps):
    imageio.mimwrite(movie_name, movie , fps = fps);    
    return None;

def CalculateProjections(video, a_x, a_y, delta_t):
    '''Returns a tupil (signal projection onto x axis, signal projection onto y axis)
    
    a_x: int coefficient, controls the peak position (x velocity component) in the frequency domain
    a_y: int coefficient, controls the peak position (y velocity component) in the frequency domain
    a_x and a_y should be large enough to move the peak from the DC component, \
        yet small enough to avoid aliasing
    delta_t: time between frames [s]
    '''       
    
    
    [nf, nr, nc] = video.shape;
    g_x = np.zeros((nf, 1), dtype = np.complex); # projection onto x axis
    g_y = np.zeros((nf, 1), dtype = np.complex); # projection onto y axis
    for frame_no in range(nf):
        temp = np.sum(video[frame_no, :, :], axis = 0).reshape(nc, 1) * \
            np.exp(1j * 2 * np.pi * a_x * np.arange(0, nc).reshape(nc, 1) * delta_t);
        g_x[frame_no] = np.sum(temp);
        
        temp = np.sum(video[frame_no, :, :], axis = 1).reshape(nr, 1) * \
            np.exp(1j * 2 * np.pi * a_y * np.arange(0, nr).reshape(nr, 1) * delta_t);
        g_y[frame_no] = np.sum(temp);    
        
    return g_x, g_y;    
    
def CalculateSpectra(g_x, g_y):
    '''Returns a tupil (fft of the signal projections onto x axis, fft of the signal projections onto y axis)
    
    g_x: signal projection onto x axis
    g_y: signal projection onto y axis
    '''    
    
    G_x = np.abs(np.fft.fft(g_x, axis = 0));
    G_y = np.abs(np.fft.fft(g_y, axis = 0));
    
    return G_x, G_y;