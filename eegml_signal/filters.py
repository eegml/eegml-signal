# -*- coding: utf-8 -*-

# easy to use filters
# see FIR filter design with Python and Scipy: by Matti Pastell
#     url = http://mpastell.com/2010/01/18/fir-with-scipy/
# given a FIR filter which has N taps, the dealy is N-2(2*Fs)
# see https://www.martinos.org/mne/stable/auto_tutorials/plot_background_filtering.html
r"""## filter use guidence
see https://allsignalprocessing.com/category/lessons/fir-filter-design/
for FIR low-pass filters, see Fred Harris function below

All signal processing has a quick discussion on choice of filters
https://allsignalprocessing.com/selecting-a-filter-which-one/

Material below is from "How to chose the number of taps (orde r= N-1 for fir)?"
source: https://dsp.stackexchange.com/questions/31066/how-many-taps-does-an-fir-filter-need

### Bellanger formula

Citing Bellanger's classic *Digital Processing of Signals: Theory and
Practice*, the point is not where your cut-off frequency is, but how
much attenuation you need, how much ripple in the signal you want to
preserve you can tolerate and, most importantly, how narrow your
transition from pass- to stopband (transition width) needs to be.

I assume you want a linear phase filter (though you specify minimum
latency, I don't think a minimum phase filter is a good idea, in
general, unless you know damn well what you're going to be doing with
your signal afterwards). In that case, the filter order (which is the
number of taps) is

$$ N ~ \frac{2}{3} log10[frac{1}{10 \delta_1 \delta_2] \fract{f_s}{\Delta f} $$

with

     $f_s$  the sampling rate 
            
$\Delta f$  the transition width, ie. the difference between end of
            pass band and start of stop band
            
$\delta_1$  the ripple in passband, ie. "how much of the original
            amplitude can you afford to vary"

$\deta_2$   the suppresion in the stop band.

Let's plug in some numbers! You specified a cut-off frequency of
$f_s/100$, so I'll just go ahead and claim your transition width will
not be more than half of that, so

     $$\Delta f = f_s/200$$

In SDR/RF land, 60 dB of suppression is typically fully sufficient ---
hardware without crazy costs, won't be better at keeping unwanted
signals out of your input, so meh, let's not waste CPU on having a
fantastic filter that's better than what your hardware can do. hence,

     $$\delta_2 = -60 dB = 10^{-6}$$

Let's say you can live with a amplitude variation of 0.1% in the
passband (if you can live with more, also consider making the
suppression requirement less strict). That's d1=10-4.

So, plugging this in:

```python
from math import log10

N = 2/3*(-log10*(10 * 10**(-4) * 10**(-6)) * f_s/(f_s/200)
  = 2/3*(log10( 10**9) * 200 
  = 2/3*9*200 = 6*200 = 1200
```

### Fred Harris rule of thumb

For a quick and very practical estimate, I like fred harris' rule-of-thumb:

Ntaps = Atten/(22*BT)

where:

   Atten is the desired attenuation in dB,

   BT is the normalized transition band:  BT = (Fstop-Fpass)/Fs,

   Fstop and Fpass are the stop band and pass band frequencies in Hz and

   Fs is the sampling frequency in Hz.

This comes out very close to what you would get for a linear phase
filter with a passband ripple of 0.1 dB. I use this rule of thumb
often to get a first cut idea of the number of taps needed, and then
modify through iteration in the filter design process.

Also to note: this rule-of-thumb provides great insight into what
really drives the number of taps: stop band attenuation and the
steepness of the transition band (and passband ripple, but typically-
at least for filters I have had to design for wireless comm
applications - the attenuation requirement would dominate over
ripple). So your question in stating a cutoff at Fs/100 is missing how
quickly you need to transition to a stop band.

Example: 60 dB attenuation, Fs=100KHz, Fpass = 1KHz, Fstop=3KHz

Ntaps = 60/(22*2/100) =137 taps (rounding up)

Playing around with these numbers can also demonstrate the
significance in processing reduction by using decimation approaches.

Adding to the accepted answer, a few additional references. I won't
write the formulas which can be involved. Those formulae mostly yield
rule-of-thumbs or approximations to start from. You can fiddle around
these numbers for your actual design.

One of the origin for Bellanger's design is: On computational
complexity in digital filters, 1981, Proc. Eur. Conf. Circuit Theory
Design, M. Bellanger. It is quite difficult to obtain, but it is
doable. Interestingly, it also specify formulae to evaluate the number
of bits per coefficient, which should be considered in
finite-arithmetic implementation. A more accessible version in French
is: Evaluation de la complexité des filtres numériques, 1982.

Several other formulae are gathered in Finite impulse response filter
design, Handbook for digital signal processing, 1993, T. Samamaki.

More recently, you can read Accurate estimation of minimum filter
length for optimum FIR digital filters, 2000, K. Ichige et al.

Last, the paper Efficient design of FIR filters with minimum filter
orders using l0-norm optimization, 2014 claims a design where the
order is gradually decreased.

"""

from __future__ import division
import math

from builtins import range
from builtins import object
import scipy
import scipy.signal
import numpy as np


def calc_ratios(f0hz, fs):
    """
    convert a frequency in Hz into the normalized frequency relative to the nyquist fs/2.0
    
    """
    return f0hz / (fs / 2.0)


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
    orderN = (fs / df) * 20 * math.log10(d2) / 22


# think about crossover point to using fft
class AbstractDigitalFilter(object):
    arr_coef = None

    def filter(self, x):
        pass

    def filtfilt(self, x):
        pass


class LowPassIdealizedFilter(object):
    """FIR lowpass filter using idealized window approach
    generally not a good choice because of distortion/artifacts
    f0hz cutoff frequency in hz
    fs sample rate

    designed using ideal filter method from scipy

    Note this produces a lot of distortion because of the rapid cutoffs

    """

    def __init__(self, f0hz, fs=1.0, order=0, window="hamming"):
        # self.setup_params(f0hz, fs, order, window)
        self.fs = fs
        self.f0hz = f0hz
        if order == 0:
            nf = int((2.0 / f0hz) * fs)
            order = nf
        self.ratiof = self.f0hz / (fs / 2.0)
        self.arr_coef = scipy.signal.firwin(order, cutoff=self.ratiof, window=window)

        # other options: firwin2
        # iirdesign
        # bessel(N,Wn)

    def setup_params(self, f0hz, fs=1.0, order=0, window="hamming"):
        self.fs = fs
        self.f0hz = f0hz
        if order == 0:
            nf = int((2.0 / f0hz) * fs)
            order = nf
        self.order = order
        self.ratiof = self.f0hz / (fs / 2.0)

    def filter(self, x):
        return scipy.signal.lfilter(self.arr_coef, 1, x)  # axis=-1, zi=None

    def filtfilt(self, x):
        return scipy.signal.filtfilt(self.arr_coef, [1], x)


class HighPassFilter(LowPassIdealizedFilter):
    """FIR lowpass filter using idealized window approach
    generally not a good choice because of distortion/artifacts
    f0hz cutoff frequency in hz
    fs sample rate

    designed using ideal filter method from scipy with spectral inversion applied

    Note this produces a lot of distortion because of the rapid cutoffs

    """

    def __init__(self, f0hz, fs=1.0, order=5, window="hamming"):
        LowPassIdealizedFilter.__init__(self, f0hz, fs, order, window="hamming")
        # now do spectral inversion
        self.arr_coef = -self.arr_coef

        a = self.arr_coef
        a[order / 2] = a[order / 2] + 1
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
        self.sigma = fs / f0hz  # sigma as 1/(normalized freq)
        self.ratiof = self.f0hz / (fs / 2.0)
        order = 8 * self.sigma
        self.order = order
        self.arr_coef = scipy.signal.gaussian(self.order, self.sigma)
        # this normalization isn't great stability wise but it makes it a norm one vector
        # self.arr_coef = self.arr_coef/sqrt(sum(self.arr_coef**2))
        self.arr_coef = self.arr_coef / sum(self.arr_coef)


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
        return scipy.signal.lfilter(taps, [1], x)

    return func


def fir_lowpass_remez_zerolag(fs, cutoff_freq, transition_width, numtaps):
    """
    return a function with optimized fir filtering
    this will not induce a lag but applies filter twice (forward and backward)

    """

    Fbands = [0, cutoff_freq, cutoff_freq + transition_width, 0.5 * fs]
    Fgains = [1, 0]
    taps = scipy.signal.remez(numtaps, Fbands, Fgains, Hz=fs)

    def func(x):
        return scipy.signal.filtfilt(taps, [1], x)

    return func


def fir_highpass_remez(fs, cutoff_freq, transition_width, numtaps):

    Nyquistfreq = 0.5 * fs
    Fbands = [0, cutoff_freq - transition_width, cutoff_freq, Nyquistfreq]
    Fgains = [0, 1]
    taps = scipy.signal.remez(numtaps, Fbands, Fgains, Hz=fs)

    def func(x):
        return scipy.signal.lfilter(taps, [1], x)

    return func


def fir_lowpass_firwin_ff(fs, cutoff_freq, numtaps):
    Nquistfreq = 0.5 * fs

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
    if not numtaps % 2:  # if even
        numtaps = numtaps + 1
    taps = scipy.signal.firwin(
        numtaps, cutoff=cutoff_freq, pass_zero=False, fs=fs
    )  # window='hamming'

    def func(x):
        return scipy.signal.filtfilt(taps, [1], x)

    return func


def fir_highpass_remez_zerolag(fs, cutoff_freq, transition_width, numtaps):
    # Fbands = [0, cutoff_freq, cutoff_freq + transition_width, 0.5*fs]

    Nyquistfreq = 0.5 * fs
    Fbands = [0, cutoff_freq - transition_width, cutoff_freq, Nyquistfreq]
    Fgains = [0, 1]
    taps = scipy.signal.remez(numtaps, Fbands, Fgains, Hz=fs)

    def func(x):
        return scipy.signal.filtfilt(taps, [1], x)

    return func


def notch_filter_iir_ff(notch_freq, fs, Q=30.0):
    nyquist = fs / 2.0
    w0 = notch_freq / nyquist  # normalized frequency
    q = Q / 2.0

    b, a = scipy.signal.iirnotch(w0, q)

    def filter_func(x):
        return scipy.signal.filtfilt(b, a, x)

    return filter_func


def highpassRC(x, dt, RC):
    """
    a simple RC high-pass filter code, naive implementation

    y[ii] = alpha*y[ii-1] + alpha (x[ii] -x[ii-1])
    """
    alpha = RC / (RC + dt)
    y = np.zeros(x.shape, dtype=x.dtype)
    y[0] = 0.0
    for ii in range(1, n):
        y[ii] = alpha * (y[ii - 1] + x[i] - x[i - 1])


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

    def __init__(
        self,
        fs=1.0,
        passfreqs=[1.0, 10.0],
        stopfreqs=[],
        gstop=60,
        gpass=1,
        order=0,
        ftype="ellip",
        window="hamming",
    ):
        # b,a = scipy.signal.iirdesign(wp = [0.05, 0.3], ws= [0.02, 0.35], gstop= 60, gpass=1,
        #                   ftype='ellip')
        # wp=[0.1,0.4],ws=[0.05,0.45], gstop=60, gpass=1, ftype='bessel'):
        self.ftype = (
            ftype
        )  # options are 'ellip', 'butter', 'cheby1', 'cheby2', 'bessel'
        nyquist = fs / 2.0
        wp = [ff / nyquist for ff in passfreqs]
        if not stopfreqs:  # then give some naive defaults
            ws = [wp[0] / 2.0, (wp[1] + nyquist) / 2.0]
        else:
            ws = [ff / nyquist for ff in stopfreqs]

        self.ba = scipy.signal.iirdesign(
            wp=wp, ws=ws, gstop=gstop, gpass=gpass, ftype=ftype
        )

    def lfilter(self, x):
        return scipy.signal.lfilter(self.ba[0], self.ba[1], x)

    def filtfilt(self, x):
        return scipy.signal.filtfilt(self.ba[0], self.ba[1], x)


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

    Nyq = Fs / 2.0
    wp = lpcf / Nyq
    ws = lpsf / Nyq

    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(ord, Wn, btype="lowpass")

    def func(x):
        return scipy.signal.lfilter(b, a, x)

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

    Nyq = Fs / 2.0
    wp = lpcf / Nyq
    ws = lpsf / Nyq

    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(ord, Wn, btype="lowpass")

    def func(x):
        return scipy.signal.filtfilt(b, a, x)

    return func


def bandpass(lpsf, lpcf, hpcf, hpsf, Fs, gpass=3, gstop=20):
    """
    FUNC: bandpass
    DESCR: return a butterworth bandpass filter
    """
    Nyq = Fs / 2.0
    wp = [lpcf / Nyq, hpcf / Nyq]
    ws = [lpsf / Nyq, hpsf / Nyq]
    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(ord, Wn, btype="bandpass")  # pun intended

    def func(x):
        return scipy.signal.lfilter(b, a, x)

    return func


def bandpass2(lpsf, lpcf, hpcf, hpsf, Fs, gpass=3, gstop=20):
    """
    FUNC: bandpass
    DESCR: return a butterworth bandpass filter
    """
    Nyq = Fs / 2.0
    wp = [lpcf / Nyq, hpcf / Nyq]
    ws = [lpsf / Nyq, hpsf / Nyq]
    ord, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)
    b, a = scipy.signal.butter(ord, Wn, btype="bandpass")  # pun intended

    def func(x):
        return scipy.signal.filtfilt(b, a, x)

    return func


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.rcParams["figure.figsize"] = (11, 8)
    plt.rcParams["figure.dpi"] = 200

    fs = 200.0
    si = 1.0 / fs  #
    nyqfreq = fs / 2.0

    t = np.arange(0.0, 10.0, si)  # 10 seconds of time
    # frequency starts at 1Hz and by 10.0s reaches 80Hz
    chrp = scipy.signal.chirp(t, 1.0, 10.0, 80.0)

    gf = GaussianLowPassFilter(f0hz=20, fs=fs)
    gfchrp = gf.filter(chrp)

    fig, axs = plt.subplots(2, 1, sharex=True)
    axs[0].plot(t, chrp)

    axs[1].plot(t, gfchrp)

    # now try lowpass2
    lpass = lowbutter2(20.0, 23.0, fs)
    lp_chrp = lpass(chrp)
    fig.savefig("gaussian_lowpass.svg")

    fig, axs = plt.subplots(3, 1)
    axs[0].plot(t, chrp)
    axs[1].plot(t, lp_chrp)
    axs[2].specgram(chrp, Fs=fs)
    plt.title("butter lowpass")

    fig.savefig("butter_lowpass.svg")

    # now look at notch filter
    notch_filter = notch_filter_iir_ff(notch_freq=60.0, Q=60, fs=fs)
    notch_chrp = notch_filter(chrp)

    fig, axs = plt.subplots(3, 1)
    axs[0].plot(t, chrp)
    axs[1].plot(t, notch_chrp)
    axs[2].specgram(notch_chrp, Fs=fs)
    fig.savefig("notch_chirp.svg")

    # test out firwin on 200Hz sample rate
    # self._highpass_cache['0.1 Hz'] = esfilters.fir_highpass_firwin_ff(self.fs, cutoff_freq=0.1,
    #                                                                   numtaps=int(self.fs))

    # h = signal.firwin(numtaps, cutoff=[55.0, 65.0], pass_zero=True, fs=fs)
    # see scipy.signal.iirnotch
    # self._highpass_cache['0.3 Hz'] = esfilters.fir_highpass_firwin_ff(self.fs, cutoff_freq=0.3,
    # numtaps=int(self.fs))

    # #ff = esfilters.fir_highpass_remez_zerolag(fs=self.fs, cutoff_freq=1.0, transition_width=0.5, numtaps=int(2*self.fs))
    # ff = esfilters.fir_highpass_firwin_ff(fs=self.fs, cutoff_freq=1.0, numtaps=int(2*self.fs))
    # self._highpass_cache['1 Hz'] = ff
    # #ff = esfilters.fir_highpass_remez_zerolag(fs=self.fs, cutoff_freq=5.0, transition_width=2.0, numtaps=int(0.2*self.fs))
    # ff = esfilters.fir_highpass_firwin_ff(fs=self.fs, cutoff_freq=5.0, numtaps=int(0.2*self.fs))
    # self._highpass_cache['5 Hz'] = ff

    # firstkey = '1 Hz' # list(self._highpass_cache.keys())[0]
    # self.current_hp_filter = self._highpass_cache[firstkey]

    # self._lowpass_cache = OrderedDict()
    # self._lowpass_cache['None'] = None
    # self._lowpass_cache['15 Hz'] = esfilters.fir_lowpass_firwin_ff(fs=self.fs, cutoff_freq=15.0, numtaps=int(self.fs/2.0))
    # self._lowpass_cache['30 Hz'] = esfilters.fir_lowpass_firwin_ff(fs=self.fs, cutoff_freq=30.0, numtaps=int(self.fs/4.0))
    # self._lowpass_cache['50 Hz'] = esfilters.fir_lowpass_firwin_ff(fs=self.fs, cutoff_freq=50.0, numtaps=int(self.fs/4.0))
    # self._lowpass_cache['70 Hz'] = esfilters.fir_lowpass_firwin_ff(fs=self.fs, cutoff_freq=70.0, numtaps=int(self.fs/4.0))
