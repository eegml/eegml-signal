# once again this has a sort of pipeline to it
"""
basically we have a source vector valued signal
s[M,N]  where M is the number of signals and N is their length
fs = sample frequency
si = 1.0/fs

sf = filtered(s) # e.g. typical EEG signal 1-70 Hz band passs

triggersignal = s[trig,:]
tf = filtered(


samp2sec()
sec2samp()


"""
from __future__ import absolute_import

from . import spikedetection
