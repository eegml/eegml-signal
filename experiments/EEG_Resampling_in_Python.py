
# coding: utf-8

# # Audio resampling in Python
# 
# *by Joachim Thiemann, 11.8.2016, joachim.thiemann@uni-oldenburg.de*
# 
# One of the most basic tasks in audio processing anyone would need to do is resampling audio files; seems like the data you want to process is _never_ sampled in the rate you want.  44.1k? 16k? 8k? Those are the common ones; there are some really odd ones out there.
# 
# Resampling is actually quite hard to get right.  You need to properly choose your antialias filters, and write a interpolation/decimation procedure that won't introduce too much noise.  There have been books written on this topic.  For the most part, there is no single univeral way to to this right, since context matters.
# 
# For a more detailed discussion on sample rate conversion see the aptly named "Digital Audio Resampling Homepage" [https://ccrma.stanford.edu/~jos/resample/].  Then look at [http://src.infinitewave.ca/] for a super informative comparison of a ton of resampling implementations.  _No seriously, go there._  (It inspired me to compare the methods below using a sine sweep.)
# 
# MATLAB has the built-in `resample` function.  Everyone uses it.  It works, but also sucks in many aspects - a much better function is in the DSP toolbox, but as near as I can tell, noone uses it (even when copious other parts of the DSP toolbox are being used!)
# 
# But I'm not talking about MATLAB, I'm talking about Python here, and it doesn't have a default resampling method - except if you're doing any kind of numerical computing, you'll be using `numpy` and probably `scipy` --- and the latter _has_ a built-in resample function.
# 
# To get ahead of myself a bit, `scipy.signal.resample` *sucks* _for audio resampling_.  That becomes apparent quite quickly - it works in frequency domain, by basically truncation or zero-padding the signal in the frequency domain.  This is quite ugly in time domain (especially since it assumes the signal to be _circular_).
# 
# There are two alternatives I want to point at that are "turn-key", that is, you just have to specify your resampling ratio, and the library does the rest.  I know of a few others, but at the time of writing this they didn't seem as easy to use (eg. just doing the interpolation/decimation, but not calculating a filter.)  If there are other notable libraries I should know of, please mention it in the comments of the blog version of this notebook [http://signalsprocessed.blogspot.com/2016/08/audio-resampling-in-python.html].
# 
# The first alternative is `scikit.resample`.  Using it has two problems: it relies on an external (C-language) library called "Secret Rabbit Code" (SRC as in "sample rate conversion", geddit?) aka libsamplerate.  Not a problem in itself, but you need to install it and this step is not automated in pip and friends (as far as I know at time of writing).  (Problem for me was that I needed to run it on a platform where I couldn't do this easily.)  Problem 2: scikit.resample 0.3.3 is Python 2 only, and the Python 3 version is unofficial (0.4.0-dev, I used [https://github.com/gregorias/samplerate]).
# 
# The other one is `resampy`, which can be found in PyPI or [https://github.com/bmcfee/resampy].  It is easy to install and works with Python 3 (`librosa` now uses it as preferred resampler over libsamplerate)
# 
# TL;DR: if you can install external libs, use scikit.resample (0.4.0-dev). `resampy` is faster, but not as good, but entirely reasonable.  (If MATLAB `resample` is good enough for you, `resampy` will serve you just fine and is easier to install)
# 
# Now for a comparison with pretty pictures.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
import scipy

import scikits.samplerate as sk_samplerate
import scipy.signal as scipy_signal
import resampy

print('scikits-samplerate (libsrc):', sk_samplerate.__version__)
print('scipy:', scipy.__version__)
print('resampy:', resampy.__version__)


# ## Downsampling a sweep
# 
# A common task is to convert between the CD sampling rate of 44.1 kHz, and the multiples of 8kHz that originated from the telekon industry.  In particular, 48kHz.  (Supposedly the rate of 44.1k was chosen in part _because_ is was difficult to convert to 48 kHz; but it is also connected to NTSC timing).  So let's have a sweep sampled at 48 kHz.

# In[6]:


P = 512
Q = 200

offset = 2000
upper_freq = 2000
instfreq = np.exp(np.linspace(np.log(offset+100), np.log(offset+upper_freq), P*2))-offset
deltaphase = 2*np.pi*instfreq/P 
cphase = np.cumsum(deltaphase)
sig = np.sin(cphase)
print('size:', sig.size)

# In[7]:


def plot_parts(w):
    plt.figure(figsize=(15,9))
    plt.subplot(3,1,1)
    plt.plot(w[:5000])
    plt.subplot(3,1,2)
    plt.plot(w[5000:10000])
    plt.subplot(3,1,3)
    plt.plot(w[-5000:])
    
plot_parts(sig)


# In[6]:


plt.figure(figsize=(15,3))
plt.specgram(sig*22, scale='dB', Fs=48000, NFFT=256)
plt.colorbar()
_=plt.axis((0,2,0,24000))


# In[7]:


plot_parts(sig)


# Now convert it to 44.1 kHz using the different libraries, and plot the spectrograms.

# In[8]:


plt.figure(figsize=(15,3))
sig1 = sk_samplerate.resample(sig, Q/P, 'sinc_best') 
#
plt.specgram(sig1*24, scale='dB', Fs=44100, NFFT=256)
plt.colorbar()
_=plt.axis((0,2,0,22500))


# In[9]:


plot_parts(sig1)


# `scikit.samplerate` (or `libsamplerate` AKA "Secret Rabbit Code") does it well. Almost no aliasing, yet close to Nyquist, and noise levels in line with the input.  Note that once the sweep is above Nyquist, the output is basically nil.

# In[10]:


plt.figure(figsize=(15,3))
sig2 = scipy_signal.resample(sig, int(len(sig)*Q/P))
plt.specgram(sig2*30, scale='dB', Fs=44100, NFFT=256)
plt.colorbar()
_=plt.axis((0,2,0,22500))


# In[11]:


plot_parts(sig2)


# And this is `scipy.signal.resample`.  Throughout the entire signal there is a high-frequency tone, and there is considerable energy even if the sweep is above Nyquist.  This is a result of the frequency-domain processing operating on the entire signal at one.  This is NOT suited to audio signals.

# In[12]:


plt.figure(figsize=(15,3))
sig3 = resampy.resample(np.float64(sig), P, Q)
plt.specgram(sig3*40, scale='dB', Fs=44100, NFFT=256)
plt.colorbar()
_=plt.axis((0,2,0,22500))


# In[13]:


plot_parts(sig3)


# Finally, `resampy`.  There are some funny nonlinear effects, but at very low level - for audio applications generally nothing to worry about.  Even the aliasing is below -60 dB.  So, while not as good as `scikit.resample` is is useable and certainly better than `scipy.signal.resample`!
# 
# ## Upsampling an impulse
# 
# A way to examine the antialias filter is to upsample an impulse.  Here, note a frustrating aspect of all these differing libraries: the interface is completely different beween all of them; and to boot, `resampy` and `scikit.resample` give different length outputs for the same upsampling ratio.  This means you can't just switch between them using a `from foo import resample` statement, you'll need a wrapper function if you want to switch freely amongst them (see `librosa` as an example).

# In[14]:


impulse = np.zeros(1000)
impulse[499] = 1

us1 = sk_samplerate.resample(impulse, P/Q, 'sinc_best')
us2 = scipy_signal.resample(impulse, int(len(impulse)*P/Q))
us3 = resampy.resample(impulse, Q, P)

print(us1.shape, us2.shape, us3.shape)


# In[15]:


plt.figure(figsize=(17,3))
plt.magnitude_spectrum(us1, c='g', Fs=48000, scale='dB', label='scikit.resample')
plt.magnitude_spectrum(us2, c='y', Fs=48000, scale='dB', label='scipy.signal.resample')
plt.magnitude_spectrum(us3, c='b', Fs=48000, scale='dB', label='resampy')
plt.axis((20000, 24000, -120, 3))
_=plt.vlines(22050, -120, 3, colors='r', linestyles='dashed', label='22.05 kHz')
_=plt.legend()


# 'scikit.resample' certainly uses the best antialias filter, with a steep slope, allowing very little energy over Nyquist.  'resampy' is a more gentle filter (lower order, perhaps?) but decent.  'scipy.signal.resample'... well, anyways.
# 
# What do the impulse responses look like in time domain?

# In[16]:


plt.figure(figsize=(17,3))
plt.plot(us1, c='g', label='scikit.resample')
plt.plot(us2, c='y', label='scipy.signal.resample')
plt.plot(us3, c='b', label='resampy')
plt.axis((500, 600, -0.2, 1))
_=plt.legend()


# In[17]:


plt.figure(figsize=(17,3))
plt.plot(10*np.log10(np.square(us1)), c='g', label='scikit.resample')
plt.plot(10*np.log10(np.square(us2)), c='y', label='scipy.signal.resample')
plt.plot(10*np.log10(np.square(us3)), c='b', label='resampy')
plt.axis((300, 800, -60, 0))
_=plt.legend()


# Unsurprisingly, 'resampy' is the most compact, which explains the gentler cut-off.   'scikit.resample' is wider, but acceptable.  'scipy.signal.resample' sticks out like a sore thumb.
# 
# ## Speed comparison

# In[18]:


get_ipython().run_line_magic('timeit', "sk_samplerate.resample(sig, Q/P, 'sinc_best')")


# In[19]:


get_ipython().run_line_magic('timeit', 'scipy_signal.resample(np.float64(sig), int(len(sig)*Q/P))')


# In[20]:


get_ipython().run_line_magic('timeit', 'resampy.resample(np.float64(sig), P, Q)')


# And here is a notable merit of 'scipy.signal.resample'.  It is faster by an order of magnitude compared to the other methods.  I suspect that if you make sure your signals are of length $2^N$, you'll get even faster results, since it'll switch to a FFT instead of a DFT.  The other two are probably losing some speed in the passing of data from Python to C - but fundamentally, frequency domain techniques do tend to be fast.  So keep that in mind you you need speed.
# 
# ## Conclusion
# 
# I'll just repeat the above TL;DR: use scikit.resample (0.4.0-dev) if you can install libsamplerate in a sane place. Else, use `resampy`, which is faster, but not as good --- but entirely reasonable.  Use 'scipy.signal.resample' only if you really need the speed, and be aware of its shortcomings (note the circular assumption!).
