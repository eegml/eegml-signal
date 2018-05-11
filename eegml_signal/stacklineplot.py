# based on multilineplot example in matplotlib with MRI data (I think)
# uses line collections (might actually be from pbrain example)
# clm

from builtins import range
import numpy as np
from matplotlib.pyplot import *
from matplotlib.collections import LineCollection

def stackplot(marray, seconds=None, start_time=None, ylabels=None):
    """
    will plot a stack of traces one above the other assuming
    marray.shape = numRows, numSamples
    """
    tarray = np.transpose(marray)
    stackplot_t(tarray, seconds=seconds, start_time=start_time, ylabels=ylabels)



def stackplot_t(tarray, seconds=None, start_time=None, ylabels=None):
    """
    will plot a stack of traces one above the other assuming
    tarray.shape =  numSamples, numRows
    """
    data = tarray
    numSamples, numRows = tarray.shape
    # data = np.random.randn(numSamples,numRows) # test data
    # data.shape = numSamples, numRows
    if seconds:
        t = seconds * np.arange(numSamples, dtype=float)/numSamples
        #import pdb
        #pdb.set_trace()
        if start_time:
            t = t+start_time
            xlm = (start_time, start_time+seconds)
        else:
            xlm = (0,seconds)
            
    else:
        t = np.arange(numSamples, dtype=float)
        xlm = (0,numSamples)
        
    ticklocs = []
    ax = subplot(111)
    xlim(*xlm)
    # xticks(np.linspace(xlm, 10))
    dmin = data.min()
    dmax = data.max()
    dr = (dmax - dmin)*0.7 # Crowd them a bit.
    y0 = dmin
    y1 = (numRows-1) * dr + dmax
    ylim(y0, y1)

    segs = []
    for i in range(numRows):
        segs.append(np.hstack((t[:,np.newaxis], data[:,i,np.newaxis])))
        # print "segs[-1].shape:", segs[-1].shape
        ticklocs.append(i*dr)

    offsets = np.zeros((numRows,2), dtype=float)
    offsets[:,1] = ticklocs

    lines = LineCollection(segs, offsets=offsets,
                           transOffset=None,
                           )

    ax.add_collection(lines)

    # set the yticks to use axes coords on the y axis
    ax.set_yticks(ticklocs)
    #ax.set_yticklabels(['PG3', 'PG5', 'PG7', 'PG9'])
    if not ylabels:
        ylabels = ["%d" % ii for ii in range(numRows)]
    ax.set_yticklabels(ylabels)
    

    xlabel('time (s)')

def test_stacklineplot():
    numSamples, numRows = 800, 5
    data = np.random.randn(numRows, numSamples) # test data
    stackplot(data, 10.0)
