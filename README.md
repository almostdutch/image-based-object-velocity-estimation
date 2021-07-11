demo_velocity_estimation_1.py <br/>

This demo shows how to estimate the velocity of a moving object (x and y components, pixels / frame) <br/>
    in the frequency domain based on the uniformly acquired frames
        
This demo uses a simulation: a moving UFO is superimposed on the image of moon <br/>
    
A sequence of uniform frames (20 fps):<br/>
<p align="center">
  <img src="video/UFO_movie.gif" width="520" height="420"/>
</p>

FFT spectra:<br/>
<p align="center">
  <img src="video/UFO_spectra.png" width="520" height="420"/>
</p>

UFO
Given:
 V_x = 3.00 [pixels / frame] V_y = 2.00 [pixels / frame]
Calculated:
 V_x = 3.00 [pixels / frame] V_y = 2.00 [pixels / frame]
 



demo_velocity_estimation_2.py <br/>

This demo shows how to estimate the velocity of a moving object (x and y components, pixels / frame) <br/>
    in the frequency domain based on the uniformly acquired frames <br/>
    
This demo uses a real video of the international space station (ISS) transitting between <br/>
    earth and moon <br/>
Video copyright: Matt Skuta (https://www.youtube.com/watch?v=bl9KHmoRGi0) <br/>
    
    
A sequence of uniform frames (20 fps):<br/>
<p align="center">
  <img src="video/ISS_movie.gif" width="520" height="420"/>
</p>

FFT spectra:<br/>
<p align="center">
  <img src="video/ISS_spectra.png" width="520" height="420"/>
</p>

ISS
Calculated:
 V_x = 2.30 [pixels / frame] V_y = 3.24 [pixels / frame]
