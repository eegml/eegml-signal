# -*- coding: utf-8 -*-
#%%
# %matplotlib inline
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import scipy

import scikits.samplerate as sk_samplerate

import eeghdf
import eegvis.stacklineplot as stackplot
#%%
# check versions
print('scikits.samplerate (Secret Rabbit code) version:', sk_samplerate.__version__)
print('scipy:', scipy.__version__)
print('matplotlib.__version__')
#%%
plt.rcParams['figure.figsize'] = (24,9)

#%%

hf = eeghdf.Eeghdf('/home/clee/eegml/eeg-hdfstorage/data/absence_epilepsy.eeghdf')
hf.phys_signals.shape

eegsig = hf.phys_signals[0:30, 0:100000]
eegsigt = eegsig.transpose()
#%%

fs0 = hf.sample_frequency # usually 200
fs1 = 156
fs2 = 100
fs3 = 50

A = 0
B = 5
#%%
stackplot.stackplot_t(eegsigt[0:int(20000),0:5])
#%% Cell[] 
eegdownt1 = sk_samplerate.resample(eegsigt, fs1/fs0, 'sinc_best', verbose=True)
eegdownt2 = sk_samplerate.resample(eegsigt, fs2/fs0, 'sinc_best', verbose=True)

print('eegdownt1.shape:', eegdownt1.shape)
#%%
stackplot.stackplot_t(eegdownt1[0:int(20000*(fs1/fs0)),0:5])
#%%

stackplot.stackplot_t(eegdownt2[0:int(20000*(fs2/fs0)),0:5])

#%%
eegdownt3 = sk_samplerate.resample(eegsigt, fs3/fs0, 'sinc_best')
stackplot.stackplot_t(eegdownt3[0:int(20000*(fs3/fs0)),0:5])
print('ratio:', fs3/fs0)
#%%
fs4 = 15
eegdownt4 = sk_samplerate.resample(eegsigt, fs4/fs0, 'sinc_best')
stackplot.stackplot_t(eegdownt4[0:int(20000*(fs4/fs0)),0:5])
#%%

fs5 = 10
eegdownt5 = sk_samplerate.resample(eegsigt, fs5/fs0, 'sinc_best')
stackplot.stackplot_t(eegdownt5[0:int(20000*(fs5/fs0)),0:5])
#%%