from __future__ import division, print_function, unicode_literals, absolute_import
# mpastell.com
# source:
# http://mpastell.com/2009/11/05/iir-filter-design-with-python-and-scipy/
from past.utils import old_div
import scipy.signal as signal
#from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from numpy import log10, unwrap, arctan2, imag, real, repeat, arange

def mfreqz(b,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20 * log10 (abs(h))
    plt.subplot(211)
    plt.plot(old_div(w,max(w)),h_dB)
    plt.ylim(-150, 5)
    plt.ylabel('Magnitude (db)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Frequency response')
    plt.subplot(212)
    h_Phase = unwrap(arctan2(imag(h),real(h)))
    plt.plot(old_div(w,max(w)),h_Phase)
    plt.ylabel('Phase (radians)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Phase response')
    plt.subplots_adjust(hspace=0.5)
    plt.show()

def impz(b,a=1):
    impulse = repeat(0.,50); impulse[0] =1.
    x = arange(0,50)
    response = signal.lfilter(b,a,impulse)
    plt.subplot(211)
    plt.stem(x, response)
    plt.ylabel('Amplitude')
    plt.xlabel(r'n (samples)')
    plt.title(r'Impulse response')
    plt.subplot(212)
    step = np.cumsum(response)
    plt.stem(x, step)
    plt.ylabel('Amplitude')
    plt.xlabel(r'n (samples)')
    plt.title(r'Step response')
    plt.subplots_adjust(hspace=0.5)
    plt.show()


if __name__=='__main__':
    import matplotlib.pyplot as plt
    
    # from pylab import *
    b,a = signal.iirdesign(wp = [0.05, 0.3], ws= [0.02, 0.35], gstop= 60, gpass=1,
                           ftype='ellip')
    mfreqz(b,a)
    fig = plt.figure()
    impz(b,a)
    fig.savefig('freq_response.svg')
