#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import math
from probabilistic_lib.functions import angle_wrap

#===============================================================================
def splitandmerge(points, split_thres=0.1, inter_thres=0.3, min_points=6, dist_thres=0.12, ang_thres=np.deg2rad(10)):
    '''
    Takes an array of N points in shape (2, N) being the first row the x
    position and the second row the y position.

    Returns an array of lines of shape (L, 4) being L the number of lines, and
    the columns the initial and final point of each line in the form
    [x1 y1 x2 y2].

    split_thres: distance threshold to provoke a split
    inter_thres: maximum distance between consecutive points in a line
    min_point  : minimum number of points in a line
    dist_thres : maximum distance to merge lines
    ang_thres  : maximum angle to merge lines
    '''
    lines = split(points, split_thres, inter_thres, min_points, 0, points.shape[1]-1)
    	
    return merge(lines, dist_thres, ang_thres)

#===============================================================================
def split(points, split_thres, inter_thres, min_points, first_pt, last_pt):
    '''
    Find lines in the points provided.
    first_pt: column position of the first point in the array
    last_pt : column position of the last point in the array
    '''
    
    assert first_pt >= 0
    assert last_pt <= points.shape[1]
   
    # Check minimum number of points
    if len(points[1]) < min_points:
	return None 
    
    # Line defined as "a*x + b*y + c = 0"
    # Calc (a, b, c) of the line (prelab question)
    x1 = points[0, first_pt]
    y1 = points[1, first_pt]
    x2 = points[0, last_pt]
    y2 = points[1, last_pt]
    
    # (y1-y2)x+(x2-x1)y+(x1y2-x2y1)=0
    a = y1-y2
    b = x2-x1
    c = ( x1*y2 - x2*y1 )
    # Distances of points to line (prelab question)
    max_d = 0
    max_index = first_pt
    counter = first_pt
    for counter in range(first_pt, last_pt):
 	t_x = points[0, counter]
    	t_y = points[1, counter]	   	    	
       	t_d = abs( a*t_x + b*t_y + c ) / math.sqrt( a*a + b*b )
        if t_d > max_d:
 		max_d = t_d
   		max_index = counter
       
    #max_d = np.max(distances)
    # Check split threshold
    if max_d > split_thres and max_index<>first_pt:
        # Check sublines
        prev = split(points, split_thres, inter_thres, min_points, first_pt, max_index)
        post = split(points, split_thres, inter_thres, min_points, max_index, last_pt )
 
        # Return results of sublines
        if prev is not None and post is not None:
            return np.vstack((prev, post))
        elif prev is not None:
            return prev
        elif post is not None:
           return post
        else:
           return None

    # Do not need to split furthermore
    else:
       # Optional check interpoint distance
       for i in range(first_pt, last_pt):           
           t_x1 = points[0, i]
    	   t_y1 = points[1, i]
    	   t_x2 = points[0, i+1]
    	   t_y2 = points[1, i+1]
           disdiff = math.sqrt((t_x1-t_x2)*(t_x1-t_x2) + (t_y1-t_y2)*(t_y1-t_y2) )
	   #Check interpoint distance threshold
           if disdiff > inter_thres:
              return None
                
       # It is a good line
       return np.array([[x1, y1, x2, y2]])
        
#===============================================================================
def merge(lines, dist_thres, ang_thres):
    '''
    Merge similar lines according to the given thresholds.
    '''
    # No data received
    if lines is None:
        return None
 
    # Check and merge similar consecutive lines
    i = 0
 
    while i in range(0, lines.shape[0]-1):
        x1 = lines[i,0]
    	y1 = lines[i,1]
    	x2 = lines[i,2]
    	y2 = lines[i,3]
 	x3 = lines[i+1,0]
    	y3 = lines[i+1,1]
    	x4 = lines[i+1,2]
    	y4 = lines[i+1,3]
        # Line angles
        ang1 = (y2-y1) / (x2-x1)
        ang2 = (y4-y3) / (x4-x3)
        
        # Below thresholds?
        angdiff = ang2 - ang1
        disdiff = np.sqrt( (lines[i,2] - lines[i+1,0])**2 +  (lines[i,3] - lines[i+1,1])**2 )
        if angdiff < ang_thres and disdiff < dist_thres:
            # Joined line           
	    lines[i,:] = [x1, y1, x4, y4]
            
            # Delete unnecessary line
            lines = np.delete(lines, i+1,0)
            
        # Nothing to merge
        else:
            i += 1
            
    return lines
