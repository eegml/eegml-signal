# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
from builtins import range
from past.utils import old_div
import numpy as np

def suppression(x, thresh=100.0, fs=128):
    """figure out where there are places where the last second of x values are below thresh
    example:
    bsarr = suppression(data, thresh=bthresh, fs=srate)

    @x I think this needs to be 1 dim data signal array
    @thresh > |x|
    @fs sample rate
    """
    fx = np.abs(x) < thresh
    # print len(x), len(fx)
    bs = np.zeros(len(fx))
    count = 0
    duration = fs
    for ii in range(len(fx)):
        if fx[ii]:
            count += 1
        else:
            count = 0
        if count == duration:
            bs[ii-count:ii]=1
        elif count > duration:
            bs[ii] = 1
            
    return bs

def burst_suppresion_ratio(bsarr, fs=128, epoch=5.0):
    """iterate in 5 second epochs (by default) to determine faction of time spent in suppression
    
    @bsarr is the array of whether the signal is within a supression
        e.g. bsarr = suppression(data, thresh, fs=fs)
        
    @fs is the sample frequency [default 128 Hz]
    @epoch is the duration of an epoch [defaults to 5 seconds]
    """
    n = len(bsarr)
    duration = old_div(float(n),  fs)
    nepoch = int(old_div(duration,epoch))
    ds = epoch*fs # samples per epoch
    bsi = np.zeros(nepoch)
    for ii in range(nepoch):
        bsi[ii] = old_div(sum(bsarr[ii*ds:(ii+1)*ds]),ds)
    return bsi
