#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_velocity_estimation_2.py

This demo shows how to estimate the velocity of a moving object (x and y components, pixels / frame) \
    in the frequency domain based on the uniformly acquired frames
    
    This demo uses a real video of the international space station (ISS) transitting between \
        earth and moon
    Video copyright: Matt Skuta (https://www.youtube.com/watch?v=bl9KHmoRGi0)
    
"""

import numpy as np
from matplotlib import pyplot as plt
from velocity_estimation_utils import SaveMovie, CalculateProjections, CalculateSpectra
import skvideo.io  

fontsize = 32;
fps = 12; # frames / s
ymin, ymax = (0, 100000); # scaling for fft y axis

# load video
frames_range = range(570, 870);
videodata = skvideo.io.vread("video/ISS_original.mp4")  
video = np.array(videodata)[frames_range, :, :, 0];
nf = len(frames_range);

# remove text
for frame_no in range(nf):
    video[frame_no, 0:60, 0:120] = 0;
    video[frame_no, 0:50, 300:] = 0;

# save movie
movie_name = 'video/ISS_movie.mp4';
SaveMovie(video, movie_name, fps);

# the actual data processing
a_x = 2;
a_y = 2;
delta_t = 1 / fps;
g_x, g_y = CalculateProjections(video, a_x, a_y, delta_t);
G_x, G_y = CalculateSpectra(g_x, g_y);

n = 40; # the spectra need a bit of help to make our peaks stand out
G_x[0:n] = 0;
G_y[0:n] = 0;
G_x[-n:] = 0;
G_y[-n:] = 0;

u_x = np.argmax(G_x); # position of max peak in fft
u_y = np.argmax(G_y); # position of max peak in fft
V_x = u_x / a_x / (nf * delta_t);
V_y = u_y / a_y / (nf * delta_t);
print(f'Calculated velocity:\n V_x = {V_x:0.2f} [pixels / frame] V_y = {V_y:0.2f} [pixels / frame]');

# show fft spectra
fig_width, fig_height = 20, 10;
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(fig_width, fig_height));
ax1.plot(G_x)
ax1.set_title('G_x', fontsize = fontsize)
ax1.set_ylim([ymin,ymax])

ax2.plot(G_y)
ax2.set_title('G_y', fontsize = fontsize)
ax2.set_ylim([ymin,ymax])
