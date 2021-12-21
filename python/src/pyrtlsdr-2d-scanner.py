import pyrtlsdr.pyrtlsdr_wrapper as sdr_wrapper

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab

c_sample_rate = 1e6
c_gain = 100
c_number_of_samples = 256*1024

c_start_freq = 125e6+7.0e6
c_scanner_delta = int(c_sample_rate / 2)
c_scanner_steps = 1
c_warmup_steps = 0

c_normalize_scan = False

sdr_client = sdr_wrapper.PyRtlSdrWrapper(
    sample_rate=c_sample_rate,
    gain=c_gain
)

for _ in range(c_warmup_steps):

    print("(Warmup Scan)")
    _ = sdr_client.scan_freq(
        center_freq=c_start_freq,
        number_of_samples=c_number_of_samples
    )

for i in range(c_scanner_steps):

    target_freq = c_start_freq + i * c_scanner_delta

    samples = sdr_client.scan_freq(
        center_freq=target_freq,
        number_of_samples=c_number_of_samples
    )

    for t_i in [2048]:

        # plt.psd(samples, NFFT=128, Fs=c_sample_rate/1e6, Fc=target_freq/1e6, alpha=.6)
        pxx, frequencies = matplotlib.mlab.psd(samples, NFFT=t_i, Fs=c_sample_rate/1e6)
        pxx = 10.0*np.log10(pxx)
        frequencies += (target_freq-125e6)/1e6

        i_start = np.nonzero(frequencies > 7.0)[0][0]
        i_stop = np.nonzero(frequencies < 7.1)[-1][-1]

        pxx_2 = pxx[i_start:i_stop]
        frequencies_2 = frequencies[i_start:i_stop]

        plt.ylim([-9, -6])
        plt.plot(frequencies_2, pxx_2, alpha=0.6, label=str(t_i))

    plt.legend()
    plt.show()

    exit()

    if c_normalize_scan:
        # pxx/=np.std(pxx)
        pxx -= np.mean(pxx)
        # plt.ylim(-10, 10)
    else:
        # plt.ylim(-30, 10)
        pass
    plt.plot(frequencies, pxx, alpha=0.6)

    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Relative power (dB)')

sdr_client.destroy()
# plt.vlines(x=93.000e6/1e6, ymin=-50, ymax=10, linestyles="dotted")
# plt.vlines(x=93.700e6/1e6, ymin=-50, ymax=10, linestyles="dotted")
# plt.vlines(x=98.500e6/1e6, ymin=-50, ymax=10, linestyles="dotted")
plt.show()
