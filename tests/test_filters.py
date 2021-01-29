#%%
from __future__ import division, print_function, unicode_literals, absolute_import

import numpy as np
import scipy.signal

import eegml_signal
import eegml_signal.filters as esfilters

SAMPLE_FREQ = 200  # Hz
si = 0.005  # sample interval of 0.01 s
NYQUIST_FREQ = SAMPLE_FREQ / 2
time_array = np.arange(0.0, 10.0, si)  # 10 seconds of time
# frequency starts at 1Hz and by 10.0s reaches 40Hz
CHIRP_0_40 = scipy.signal.chirp(time_array, 1.0, 10.0, 40.0)

#%%
def test_fir_lowpass():
    # lag inducing filter
    f = esfilters.fir_lowpass_remez(
        fs=SAMPLE_FREQ,
        cutoff_freq=15,
        transition_width=3,
        numtaps=int(SAMPLE_FREQ / 15 * 4),
    )
    # f = esfilters.fir_lowpass(fs=SAMPLE_FREQ, cutoff_freq=15, transition_width=3, numtaps=int(SAMPLE_FREQ/15*4))
    result = f(CHIRP_0_40)
    return result


#%%


def test_fir_lowpass_zerolag():
    f = esfilters.fir_lowpass_remez_zerolag(
        # f = esfilters.fir_lowpass_zerolag(
        fs=SAMPLE_FREQ,
        cutoff_freq=15,
        transition_width=3,
        numtaps=int(SAMPLE_FREQ / 15 * 4),
    )
    result = f(CHIRP_0_40)
    return result


#%%
def test_fir_highpass_zerolag():
    # f = esfilters.fir_highpass_zerolag(
    f = esfilters.fir_highpass_remez(
        fs=SAMPLE_FREQ,
        cutoff_freq=15,
        transition_width=3,
        numtaps=int(SAMPLE_FREQ / 15 * 4),
    )
    result = f(CHIRP_0_40)
    return result


#%%
if __name__ == "__main__":
    import matplotlib

    matplotlib.use("PS")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(20, 10))
    N = 5
    ii = 0

    x = CHIRP_0_40
    y_lp = test_fir_lowpass()

    axs = fig.subplots(N, 1)

    axs[ii].plot(time_array, x)
    ii += 1

    axs[ii].specgram(x, Fs=SAMPLE_FREQ)
    ii += 1

    axs[ii].plot(time_array, y_lp)
    ii += 1

    y = test_fir_highpass_zerolag()

    axs[ii].plot(time_array, y)
    # axs[ii].title('high_pass zero lag')
    ii += 1

    butter_lpass = esfilters.lowbutter2(15.0, 18.0, SAMPLE_FREQ)
    butter_lp_chrp = butter_lpass(x)
    axs[4].plot(butter_lp_chrp)

    print("ii:", ii)

    plt.savefig("test_fir_lowpass.svg")

    plt.figure(figsize=(20, 10))
    plt.plot(time_array, butter_lp_chrp)
    plt.savefig("butter.svg")

# %%
