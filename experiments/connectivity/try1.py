import numpy as np
from scipy import linalg

import mne
from mne import fiff
from mne.connectivity import spectral_connectivity
from mne.datasets import sample

fiffile = '../XA005045_1-1+.fif'

raw = fiff.Raw(fiffile)