import pyrtlsdr.pyrtlsdr_wrapper as sdr_wrapper

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab

c_sample_rate = 2e6
c_gain = 100
c_number_of_samples = 256*1024

c_start_freq = 91.0e6
c_scanner_delta = int(c_sample_rate / 2)
c_scanner_steps = 9

sdr_client = sdr_wrapper.PyRtlSdrWrapper(
    sample_rate=c_sample_rate,
    gain=c_gain
)

for i in range(c_scanner_steps):

    target_freq = c_start_freq + i * c_scanner_delta

    samples = sdr_client.scan_freq(
        center_freq=target_freq,
        number_of_samples=c_number_of_samples
    )

    # plt.psd(samples, NFFT=128, Fs=c_sample_rate/1e6, Fc=target_freq/1e6, alpha=.6)
    pxx, frequencies = matplotlib.mlab.psd(samples, NFFT=128, Fs=c_sample_rate/1e6)
    pxx = 10.0*np.log10(pxx)
    frequencies += target_freq/1e6
    plt.plot(frequencies, pxx, alpha=0.6)

    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Relative power (dB)')
    plt.ylim(-30, 10)

sdr_client.destroy()
plt.vlines(x=93.000e6/1e6, ymin=-50, ymax=10, linestyles="dotted")
plt.vlines(x=93.700e6/1e6, ymin=-50, ymax=10, linestyles="dotted")
plt.vlines(x=98.500e6/1e6, ymin=-50, ymax=10, linestyles="dotted")
plt.show()
