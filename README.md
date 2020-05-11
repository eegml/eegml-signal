# eegml-signal README

A package to collect function and information about signal processing relevant to EEG waveforms.

UPDATE: torchaudio now has many useful fuctions for 1D signal processing which may replace some prior work and be easier to integrate into our end to end systems.

## Filtering
- scipy-based FIR filtering for eeg code: [eegml_signal.filters](https://github.com/eegml/eegml-signal/blob/master/eegml_signal/filters.py)

## Downsampling 
- example using resampy: [h5tuh_downsample.py](https://github.com/eegml/eegml-signal/blob/master/scripts/h5tuh_downsample_norm.py)
- check out downsampling module in [torchaudio.transforms.Resample](https://pytorch.org/audio/transforms.html#resample)

## spike detection
- early start on spike detection: [eegml_signal/spikedetection.py](https://github.com/eegml/eegml-signal/blob/master/eegml_signal/spikedetection.py)

## For wavelets:
- [kymatio](https://github.com/kymatio/kymatio) is a pytorch based wavelet scattering system
- predecessor to kymatio is [pyscatwave](https://github.com/edouardoyallon/pyscatwave/)
this is how to get the coefficients from pywt and use with pytorch: https://github.com/t-vi/pytorch-tvmisc/blob/master/misc/2D-Wavelet-Transform.ipynb
https://github.com/tomrunia/PyTorchWavelets

### To do
- [ ] add published opensource HFO detection algorithms
- [ ] test kymatio and PyTorchWavelets and torchaudio more
- [ ] improve spike detection 
