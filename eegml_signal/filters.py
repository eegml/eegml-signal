# easy to use filters
# given a FIR filter which has N taps, the dealy is N-2(2*Fs)
from __future__ import division

from builtins import range
from builtins import object
import scipy
import scipy.signal

def calc_ratios(f0hz, fs):
    """
    convert a frequency in Hz into the normalized frequency relative to the nyquist fs/2.0
    
    """
    return f0hz/(fs/2.0)

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
        
        
    
"""
A simple moving average corresponds to a uniform probability distribution and thus its filter width of size n has standard deviation \sqrt{({\sigma}^2-1)/12}. Thus m moving averages with sizes {\sigma}_1,\dots,{\sigma}_m yield a standard deviation of

    \sigma = \sqrt{\frac{{\sigma}_1^2+\cdots+{\sigma}_m^2-m}{12}}.

(Note that standard deviations do not sum up, but variances do.)
"""

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

class PassBand(object):
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
