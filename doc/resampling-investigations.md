# Different ways to resample

## general overview
if you want to downsample over view is
original signal -> filtered signal -> downsample

OR

original signal -> upsample by U 

### scipy based resampling
https://scipy-lectures.org/intro/scipy/auto_examples/plot_resample.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.resample_poly.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.resample.html

scipy.signal.resample(x, num, t=None, axis=0, window=None)
scipy.signal.resample_poly(x, up, down, axis=0, window=('kaiser', 5.0))[source]

If the window requires no parameters, then window can be a string.

If the window requires parameters, then window must be a tuple with the first argument the string name of the window, and the next arguments the needed parameters.

boxcar
triang
blackman
hamming
hann
bartlett
flattop
parzen
bohman
blackmanharris
nuttall
barthann
kaiser (needs beta)
gaussian (needs standard deviation)
general_gaussian (needs power, width)
slepian (needs width)

dpss (needs normalized half-bandwidth)

chebwin (needs attenuation)

exponential (needs decay scale)

tukey (needs taper fraction)
### secrete rabbit code based resampling


#### resampy
- resampy is pip installable, and also can be install from conda
- pip install resampy  OR  conda install resampy -c conda-forge

- it appears not to work directly on int16 or int32 arrays but you can convert first to floats

example:
```
#%%
import eeghdf
import resampy
import numpy as np
import matplotlib.pyplot as plt

hf = eeghdf.Eeghdf('./s003_t008.eeg.h5')

#%%

sr_orig = hf.sample_frequency # sr_orig = 400


sr_tar = 200  # the sampling rate to transform to

dig = hf.rawsignals  # the original digital samples dtype=int16

# In   []: dig
# Out  []: <HDF5 dataset "signals": shape (32, 331200), type "<i2">

# In []: dig.shape
# Out[]: (32, 331200)

#%%
# note need produce floating point version of array
# window='kaiser_best', window='kaiser_fast' and so on
fdig200 = resampy.resample(np.array(dig, dtype=np.float64), sr_orig, sr_tar) 

dig200 = np.array(fdig200, dtype=np.int16)

# In []: dig200.dtype
# Out[]: dtype('int16')
# In []: dig200.shape
# Out[]: (32, 165600)

#%% 
# [markdown]
# visualize the output

#%%
plt.figure()
t400 = np.arange(0,4000)
t200 = np.arange(0,4000, step=2)
plt.plot(t400, dig[0, 0:4000], label='original fs=400Hz')
plt.plot(t200, fdig200[0,0:2000], label='int16 fs=200Hz')
plt.plot(t200, dig200[0, 0:2000], label='float64 fs=200Hz')
plt.legend()
#%%
plt.show()

#%%

# to help with comparing other channels
def plot_channel(num):
    plt.figure()
    t400 = np.arange(0,4000)
    t200 = np.arange(0,4000, step=2)
    plt.plot(t400, dig[num, 0:4000], label='original fs=400Hz')
    plt.plot(t200, fdig200[num,0:2000], label='int16 fs=200Hz')
    plt.plot(t200, dig200[num, 0:2000], label='float64 fs=200Hz')
    plt.plot(t200, dig200_kbest[num, 0:2000], label='kaiser best int16 fs=200Hz')
    plt.legend()
    plt.title(f'channel {num}')
    plt.show()


```

scikits resample 

currently scikits.sample rate is required for good downsampling
the one on pypi is not going to work with python3
probably should make this point to a particular commit
it requires libsamplerate to be installed (on linux)
on ubuntu 18.04 do:
```
     sudo apt install libsamplerate-dev
```	 
```
-e git+https://github.com/cournape/samplerate/#egg=samplerate
```

### pytorch based resampling
it is important to note that pytorch torchaudio includes a resample function
in the transform section. it may be worthwhile to add this into to torch based pipelines
I have not tested it yet

