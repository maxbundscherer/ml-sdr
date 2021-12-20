import pyrtlsdr.pyrtlsdr_wrapper as sdr_wrapper
import matplotlib.pyplot as plt

c_sample_rate = 2.4e6
c_bandwidth = 1.5e6
c_gain = 100
c_number_of_samples = 256*1024

c_start_freq = 93e6
c_scanner_delta = 1e6
c_scanner_steps = 6

sdr_client = sdr_wrapper.PyRtlSdrWrapper(
    sample_rate=c_sample_rate,
    bandwidth=c_bandwidth,
    gain=c_gain
)

for i in range(c_scanner_steps):

    target_freq = c_start_freq + i * c_scanner_delta

    samples = sdr_client.scan_freq(
        center_freq=target_freq,
        number_of_samples=c_number_of_samples
    )

    plt.psd(samples, NFFT=256, Fs=c_bandwidth/1e6, Fc=target_freq/1e6)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Relative power (dB)')

sdr_client.destroy()
plt.show()
