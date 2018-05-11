# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import edflib

# <codecell>

from mne.connectivity import spectral_connectivity

# <codecell>

import numpy as np

# <codecell>

import pandas

# <codecell>

hdr = pandas.read_csv('../XA005045_1-1+_header.txt')

# <codecell>

hdr

# <codecell>

data = pandas.read_csv('../XA005045_1-1+_data.txt')

# <codecell>

data

# <codecell>

sigs = pandas.read_csv('../XA005045_1-1+_signals.txt')

# <codecell>

sigs

# <codecell>

arr = np.array(data)

# <codecell>

arr

# <codecell>

arr.shape

# <codecell>

%pylab
plot(arr[:2000, 1])

# <codecell>

%pylab inline

# <codecell>

plot(arr[:2000, 1])

# <codecell>

Fs = 200.0

# <codecell>

T = 15.0
N = T * Fs
tarr = arange(N)/Fs
plot(tarr,arr[:N, 0:4])

# <codecell>

plot(tarr,arr[:N, 0:4])

# <codecell>

figure()
t = 200
T = 10.0
N = T * Fs
tarr = arange(N)/Fs
plot(tarr,arr[t*Fs:N+t*Fs, 0:4])

# <codecell>

 data.to_hdf('XA005045_1.hdf5', 'data')

# <codecell>

hdr.to_hdf('XA005045_1.hdf5', 'header', append=True)

# <codecell>

sigs.to_hdf('XA005045_1.hdf5', 'signal_names', append=True)

# <codecell>

ls -lh

# <codecell>

ls -lh ../X*

# <codecell>

!rm compressed.hdf5
!ptrepack --chunkshape=auto --complevel=9 --complib=blosc  XA005045_1.hdf5 compresssed.hdf5

# <codecell>

ls -lh

# <codecell>

!rm -f compressed.hdf5

# <codecell>

ls -lh

# <codecell>

rm -f compresssed.hdf5

# <codecell>

dataf = data
data = np.array(data)

# <codecell>

data.shape

# <codecell>

data[1,:]

# <codecell>

plot(data[50000:54000, 1]- data[50000:54000, 10]) #Fp1-F7

# <codecell>

622.0/30

# <codecell>

4*4

# <codecell>


