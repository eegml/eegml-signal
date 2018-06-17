# easy to use filters
# see FIR filter design with Python and Scipy: by Matti Pastell
#     url = http://mpastell.com/2010/01/18/fir-with-scipy/
# given a FIR filter which has N taps, the dealy is N-2(2*Fs)
# see https://www.martinos.org/mne/stable/auto_tutorials/plot_background_filtering.html


from __future__ import division
import math

from builtins import range
from builtins import object
import scipy
import scipy.signal

def calc_ratios(f0hz, fs):
    """
    convert a frequency in Hz into the normalized frequency relative to the nyquist fs/2.0
    
    """
    return f0hz/(fs/2.0)

# see firpmord

def fred_harris_lowpass_order_guess(fs, df, d1, d2):
    """
    imagine the original gain was 1.0, then @d1 and @d2
    are the left over signal in the pass band (d1) and the stop band (d2)
    @fs - sample frequency
    @df - width of the pass band in Hz (same units as fs)

    fred harris rule of thumb for choosing order of low-pass filter 

    order N = (fs/df) * 
    orderN = (fs/delta(f)) * [atten(dB)/22]
    deflta(f) is transitionband in same units of fs,
    fs is sample rate
    atten(dB) is the target rejection in dB
    atten(dB) = 20 * log10(d2)
    d2 is the amplitude of signal ripple in the stop band
    d1 is the half-height of the ripple in the pass pand
    """
    # source:url= https://dsp.stackexchange.com/questions/37646/filter-order-rule-of-thumb
    orderN = (fs/df) * 20*math.log10(d2)/22

# think about crossover point to using fft
class AbstractDigitalFilter(object):
    arr_coef = None
    def filter(self, x):
        pass
    def filtfilt(self, x):
        pass


class LowPassIdealizedFilter(object):
    """FIR lowpass filter using idealized window approach
    f0hz cutoff frequency in hz
    fs sample rate

    designed using ideal filter method from scipy

    Note this produces a lot of distortion because of the rapid cutoffs

    """
    def __init__(self, f0hz, fs=1.0, order=0, window='hamming'):
        # self.setup_params(f0hz, fs, order, window)
        self.fs = fs
        self.f0hz = f0hz
        if order == 0:
            nf = int( (2.0/f0hz)*fs)
            order = nf
        self.ratiof = self.f0hz/(fs/2.0)
        self.arr_coef = scipy.signal.firwin(order,cutoff=self.ratiof, window=window)

        # other options: firwin2
        # iirdesign
        # bessel(N,Wn)

    def setup_params(self,f0hz, fs=1.0, order=0, window='hamming'):
        self.fs = fs
        self.f0hz = f0hz
        if order == 0:
            nf = int( (2.0/f0hz)*fs)
            order = nf
        self.order=order
        self.ratiof = self.f0hz/(fs/2.0)


    def filter(self, x):
        return scipy.signal.lfilter(self.arr_coef, 1, x) # axis=-1, zi=None

    def filtfilt(self,x):
        return scipy.signal.filtfilt(self.arr_coef, [1], x)


class HighPassFilter(LowPassIdealizedFilter):
    """FIR lowpass filter using idealized window approach
    f0hz cutoff frequency in hz
    fs sample rate

    designed using ideal filter method from scipy with spectrual inversion applied

    Note this produces a lot of distortion because of the rapid cutoffs

    """    
    def __init__(self, f0hz, fs=1.0, order=5, window='hamming'):
        LowPassIdealizedFilter.__init__(self,f0hz, fs, order, window='hamming')
        # now do spectral inversion
        self.arr_coef = - self.arr_coef

        a = self.arr_coef
        a[order/2] = a[order/2] + 1
        self.arr_coef = a
    # then use methods from LowPassIdealizedFilter


class GaussianLowPassFilter(LowPassIdealizedFilter):
    """
    >>> import eegquant.sigproc.filters
    >>> glp = GaussianLowPassFilter(f0hz, fs=1.0, order=0, window=None)


    $g(x)=\sqrt(a/\pi) e^{-a x^2}$

    $g(x) = \frac{1}{\sqrt{2\cdot\pi}\cdot\sigma}\cdot e^{-\frac{x^2}{2\sigma^2}} $

    window funciton = None at default (use naive truncation)

    Note this can be approximated quite well by 4 iterations of a moving average filter
    and that may be faster (cubic B-spline)

    The cutoff frequency is:
    $f_c = F_s/\sigma = F_s \sqrt{a}$

    Note that the fourier transform of g(x) is another gaussian:
    $F[g][f] =  e^{- (\pi)^2 f^2/a }$
    ln(1/b)  = -(\pi^2/a) f^2
    f_c = \sqrt{a lnb/ \pi^2}

    if we go for the -dB corder then b = \sqrt(2) and lnb -> 1/2*ln2
    and     a -> 1/(2*sigma^2)
    f_c = \sqrt{a 1/2 ln2 / \pi^2}
    f_c = \sqrt{ (2* \sigma^2)^(-1) 1/2 ln2 / \pi^2}
    f_c =    (1/ (\pi \sigma ) ) *  \sqrt{ 1/4 * ln2 }
        =   \sqrt{ln2} / (2 \pi \sigma)
        ~ 0.1325/sigma



    """

    def __init__(self, f0hz, fs=1.0, order=0, window=None):
        self.fs = fs
        self.f0hz = f0hz
        self.sigma = fs/f0hz # sigma as 1/(normalized freq)
        self.ratiof = self.f0hz/(fs/2.0)
        order = 8*self.sigma
        self.order=order
        self.arr_coef = scipy.signal.gaussian(self.order, self.sigma)
        # this normalization isn't great stability wise but it makes it a norm one vector
        #self.arr_coef = self.arr_coef/sqrt(sum(self.arr_coef**2))
        self.arr_coef = self.arr_coef/sum(self.arr_coef)
        
        
## try some designed FIR filters    
"""
A simple moving average corresponds to a uniform probability distribution and thus its filter width of size n has standard deviation \sqrt{({\sigma}^2-1)/12}. Thus m moving averages with sizes {\sigma}_1,\dots,{\sigma}_m yield a standard deviation of

    \sigma = \sqrt{\frac{{\sigma}_1^2+\cdots+{\sigma}_m^2-m}{12}}.

(Note that standard deviations do not sum up, but variances do.)
"""

"""
In [3]: remez?
Signature: remez(numtaps, bands, desired, weight=None, Hz=1, type='bandpass', maxiter=25, grid_density=16)
Docstring:
Calculate the minimax optimal filter using the Remez exchange algorithm.

Calculate the filter-coefficients for the finite impulse response
(FIR) filter whose transfer function minimizes the maximum error
between the desired gain and the realized gain in the specified
frequency bands using the Remez exchange algorithm.

Parameters
----------
numtaps : int
    The desired number of taps in the filter. The number of taps is
    the number of terms in the filter, or the filter order plus one.
bands : array_like
    A monotonic sequence containing the band edges in Hz.
    All elements must be non-negative and less than half the sampling
    frequency as given by `Hz`.
desired : array_like
    A sequence half the size of bands containing the desired gain
    in each of the specified bands.
weight : array_like, optional
    A relative weighting to give to each band region. The length of
    `weight` has to be half the length of `bands`.
Hz : scalar, optional
    The sampling frequency in Hz. Default is 1.
type : {'bandpass', 'differentiator', 'hilbert'}, optional
    The type of filter:

      * 'bandpass' : flat response in bands. This is the default.

      * 'differentiator' : frequency proportional response in bands.

      * 'hilbert' : filter with odd symmetry, that is, type III
                    (for even order) or type IV (for odd order)
                    linear phase filters.

maxiter : int, optional
    Maximum number of iterations of the algorithm. Default is 25.
grid_density : int, optional
    Grid density. The dense grid used in `remez` is of size
    ``(numtaps + 1) * grid_density``. Default is 16.

Returns
-------
out : ndarray
    A rank-1 array containing the coefficients of the optimal
    (in a minimax sense) filter.

See Also
--------
firls
firwin
firwin2
minimum_phase

References
----------
.. [1] J. H. McClellan and T. W. Parks, "A unified approach to the
       design of optimum FIR linear phase digital filters",
       IEEE Trans. Circuit Theory, vol. CT-20, pp. 697-701, 1973.
.. [2] J. H. McClellan, T. W. Parks and L. R. Rabiner, "A Computer
       Program for Designing Optimum FIR Linear Phase Digital
       Filters", IEEE Trans. Audio Electroacoust., vol. AU-21,
       pp. 506-525, 1973.

Examples
--------
We want to construct a filter with a passband at 0.2-0.4 Hz, and
stop bands at 0-0.1 Hz and 0.45-0.5 Hz. Note that this means that the
behavior in the frequency ranges between those bands is unspecified and
may overshoot.

>>> from scipy import signal
>>> bpass = signal.remez(72, [0, 0.1, 0.2, 0.4, 0.45, 0.5], [0, 1, 0])
>>> freq, response = signal.freqz(bpass)
>>> ampl = np.abs(response)

>>> import matplotlib.pyplot as plt
>>> fig = plt.figure()
>>> ax1 = fig.add_subplot(111)
>>> ax1.semilogy(freq/(2*np.pi), ampl, 'b-')  # freq in Hz
>>> plt.show()
File:      /usr/local/anaconda3/lib/python3.6/site-packages/scipy/signal/fir_filter_design.py
Type:      function
"""


def fir_lowpass_remez(fs, cutoff_freq, transition_width, numtaps):
    """
    return a function with optimized fir filtering
    this will induce a lag
    """
    Nyquistfreq = 0.5 * fs
    Fbands = [0, cutoff_freq, cutoff_freq + transition_width, Nyquistfreq]
    Fgains = [1, 0]
    taps = scipy.signal.remez(numtaps, Fbands, Fgains, Hz=fs)

    def func(x):
        return scipy.signal.lfilter(taps,[1], x)

    return func

def fir_lowpass_remez_zerolag(fs, cutoff_freq, transition_width, numtaps):
    """
    return a function with optimized fir filtering
    this will not induce a lag but applies filter twice (forward and backward)

    """

    Fbands = [0, cutoff_freq, cutoff_freq + transition_width, 0.5*fs]
    Fgains = [1, 0]
    taps = scipy.signal.remez(numtaps, Fbands, Fgains, Hz=fs)

    def func(x):
        return scipy.signal.filtfilt(taps,[1], x)

    return func

    
def fir_highpass_remez(fs, cutoff_freq, transition_width, numtaps):

    Nyquistfreq = 0.5 * fs
    Fbands = [0, cutoff_freq- transition_width, cutoff_freq, Nyquistfreq]
    Fgains = [0, 1]
    taps = scipy.signal.remez(numtaps, Fbands, Fgains, Hz=fs)

    def func(x):
        return scipy.signal.lfilter(taps,[1], x)

    return func

def fir_lowpass_firwin_ff(fs, cutoff_freq, numtaps):
    Nquistfreq = 0.5 *fs
    
    taps = scipy.signal.firwin(numtaps, cutoff=cutoff_freq, pass_zero=True, fs=fs)

    def func(x):
        return scipy.signal.filtfilt(taps, [1], x)

    return func


def fir_highpass_firwin_ff(fs, cutoff_freq, numtaps):
    """
    try @cutoff_freq as a float or 1D array_like
    Cutoff frequency of filter (expressed in the same units as `nyq`)
    OR an array of cutoff frequencies (that is, band edges). In the
    latter case, the frequencies in `cutoff` should be positive and
    monotonically increasing between 0 and `nyq`.  The values 0 and
    `nyq` must not be included in `cutoff`.
    """
    Nyquistfreq = 0.5 * fs
    # set pass_zero=False so DC values are not passsed
    if not numtaps % 2: # if even
        numtaps = numtaps +1
    taps = scipy.signal.firwin(numtaps, cutoff=cutoff_freq, pass_zero=False,
                               fs=fs) # window='hamming'

    def func(x):
        return scipy.signal.filtfilt(taps, [1], x)

    return func
            
def fir_highpass_remez_zerolag(fs, cutoff_freq, transition_width, numtaps):
    #Fbands = [0, cutoff_freq, cutoff_freq + transition_width, 0.5*fs]

    Nyquistfreq = 0.5 * fs
    Fbands = [0, cutoff_freq- transition_width, cutoff_freq, Nyquistfreq]
    Fgains = [0, 1]
    taps = scipy.signal.remez(numtaps, Fbands, Fgains, Hz=fs)

    def func(x):
        return scipy.signal.filtfilt(taps,[1], x)

    return func


def highpassRC(x, dt, RC):
    """
    a simple RC high-pass filter code, naive implementation

    y[ii] = alpha*y[ii-1] + alpha (x[ii] -x[ii-1])
    """
    alpha = RC/(RC+dt)
    y = np.zeros(x.shape, dtype=x.dtype)
    y[0] = 0.0
    for ii in range(1,n):
        y[ii] = alpha*(y[ii-1] + x[i] -x[i-1])


# scipy.signal.iirdesign(wp, ws, gpass, gstop, analog=0, ftype='ellip', output='ba')

class PassBandIIR(object):
    """
    b,a = scipy.signal.iirdesign(wp = [0.05, 0.3], ws= [0.02, 0.35], gstop= 60, gpass=1,
                           ftype='ellip')

    wp
    ws
    gstop
    gpass
    ftype     options are 'ellip', 'butter', 'cheby1', 'cheby2', 'bessel'


    """
    def __init__(self, fs=1.0, passfreqs=[1.0,10.0], stopfreqs=[],
                 gstop =60, gpass=1, order=0, ftype='ellip', window='hamming'):
        #b,a = scipy.signal.iirdesign(wp = [0.05, 0.3], ws= [0.02, 0.35], gstop= 60, gpass=1,
        #                   ftype='ellip')
        # wp=[0.1,0.4],ws=[0.05,0.45], gstop=60, gpass=1, ftype='bessel'):
        self.ftype = ftype # options are 'ellip', 'butter', 'cheby1', 'cheby2', 'bessel'
        nyquist = fs/2.0
        wp = [ff/nyquist for ff in passfreqs]
        if not stopfreqs: # then give some naive defaults
            ws = [wp[0]/2.0, (wp[1]+nyquist)/2.0]
        else:
            ws = [ff/nyquist for ff in stopfreqs]
            
        self.ba = scipy.signal.iirdesign(wp=wp, ws=ws, gstop=gstop, gpass=gpass, ftype=ftype)

    def lfilter(self, x):
        return scipy.signal.lfilter(self.ba[0],self.ba[1], x)

    def filtfilt(self, x):
        return scipy.signal.filtfilt(self.ba[0],self.ba[1], x)
        



# from pbrain 
def lowbutter(lpcf, lpsf, Fs, gpass=3, gstop=15):
    """
    FUNC: lowbutter
    DESCR: Return a low pass butterworth filter with
    lpcf  : lowpass corner freq
    lpsf  : lowpass stop freq
    gpass : corner freq attenuation
    gstop : stop freq attenuation    

    return value is a callable function that will filter your data

    Example:
      mybutt = lowbutter(12, 15, eeg.freq)
      sfilt = mybutt(s1)

    """
    
    Nyq = Fs/2.
    wp = lpcf/Nyq
    ws = lpsf/Nyq

    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(ord, Wn, btype='lowpass')

    def func(x):
        return scipy.signal.lfilter(b,a,x)
    return func


def lowbutter2(lpcf, lpsf, Fs, gpass=3, gstop=15):
    """
    FUNC: lowbutter
    DESCR: Return a low pass butterworth filter with
    lpcf  : lowpass corner freq
    lpsf  : lowpass stop freq
    gpass : corner freq attenuation
    gstop : stop freq attenuation    

    return value is a callable function that will filter your data
    with zero phase lag via the filtfilt 
    Example:
      mybutt = lowbutter(12, 15, eeg.freq)
      sfilt = mybutt(s1)

    """
    
    Nyq = Fs/2.
    wp = lpcf/Nyq
    ws = lpsf/Nyq

    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(ord, Wn, btype='lowpass')

    def func(x):
        return scipy.signal.filtfilt(b,a,x)
    return func

def bandpass(lpsf, lpcf, hpcf, hpsf, Fs, gpass=3, gstop=20):
    """
    FUNC: bandpass
    DESCR: return a butterworth bandpass filter
    """
    Nyq = Fs/2.
    wp = [lpcf/Nyq, hpcf/Nyq]
    ws = [lpsf/Nyq, hpsf/Nyq]
    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b,a = scipy.signal.butter(ord, Wn, btype='bandpass') # pun intended
    def func(x):
        return scipy.signal.lfilter(b,a,x)

    return func

def bandpass2(lpsf, lpcf, hpcf, hpsf, Fs, gpass=3, gstop=20):
    """
    FUNC: bandpass
    DESCR: return a butterworth bandpass filter
    """
    Nyq = Fs/2.
    wp = [lpcf/Nyq, hpcf/Nyq]
    ws = [lpsf/Nyq, hpsf/Nyq]
    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b,a = scipy.signal.butter(ord, Wn, btype='bandpass') # pun intended
    def func(x):
        return scipy.signal.filtfilt(b,a,x)

    return func


if __name__=='__main__':
    from pylab import *
    
    si = 0.01 # sample interval of 0.01 s
    fs = int(1.0/si)
    nfreq = fs/2
    t = arange(0.0,10.0,si) # 10 seconds of time 
    # frequency starts at 1Hz and by 10.0s reaches 40Hz
    chrp = scipy.signal.chirp(t, 1.0, 10.0, 40.0)

    gf = GaussianLowPassFilter(f0hz=20, fs=fs)
    gfchrp = gf.filter(chrp)

    fig,axs =subplots(2,1,sharex=True)
    axs[0].plot(t,chrp)

    axs[1].plot(t, gfchrp)
    
    # now try lowpass2
    lpass = lowbutter2(20.0, 23.0, fs)
    lp_chrp = lpass(chrp)
    
    fig,axs = subplots(3,1)
    axs[0].plot(t,chrp)
    axs[1].plot(t, lp_chrp)
    axs[2].specgram(chrp, fs=fs)
    title('butter lowpass')
