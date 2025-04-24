# **********************************************************************
# Name : Random Tape Splitter                                                                    
# version : 1.0
# Author : Damien Vallet
# Role : This script simulates the process of cutting a tape into pieces, 
#        throwing it away, and splicing it back randomly. It was inspired 
#        by old tape machines generative music techniques.
# Licence : MIT License (MIT)
# Usage : <python> <script> <path/to/file> <number of split>
# **********************************************************************

import os
import numpy as np
import soundfile as sf
import random
import math
import scipy.signal as sg

def randomStartPoint(N):
    """ get a random start point between [0, N] """
    x = math.floor(random.random() * N) 
    return x 

def randomSize(max_lim):
    """ get a random size chunk between [0, max size of split] """
    x = math.floor(random.random() * max_lim)
    return x

def coinFlip():
    """ return 1/2 True or False"""
    if random.random() > 0.5:
        return True
    else:
        return False

def reverseArray(data):
    """ return a reversed array accroding to coinFlip """
    if coinFlip():
        arr = np.flip(data, axis=0)
        return arr
    else:
        return data

def limitEnd(start, max_lim, N):
    """ limit size of chunk to avoid copying inexistent value """
    end = start + randomSize(max_lim)
    if end > N:
        return N
    else:
        return end
   
def main(audiofile, split):
    """ this scripts simulate the process of cutting a tape 
        into pieces throwing it away and splicing it back randomly 
    
    """
    x, fs = sf.read(audiofile)
    filename, ext = os.path.splitext(os.path.basename(audiofile))
    N = len(x)
    y = np.zeros(0)
    max_lim = N // split

    for k in range(split):   
        start = randomStartPoint(N)
        end = limitEnd(start, max_lim, N)
        data, sr = sf.read(audiofile, always_2d=True, frames=-1, start=start, stop=end)
        rev_data = reverseArray(data)    
        M = len(rev_data)        
        w = sg.get_window(("tukey", 0.1),M)        
        rev_data *= w.reshape(M, 1)           
        y = np.append(y, rev_data)

    sf.write(f"{filename}-{k}.wav", y, fs)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        audiofile = sys.argv[1]
        split = int(sys.argv[2])
        main(audiofile, split)
    else:
        print("usage: <python> <script> <path/to/file> <number of split>")
