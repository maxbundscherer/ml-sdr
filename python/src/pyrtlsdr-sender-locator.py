import pyrtlsdr.pyrtlsdr_wrapper as sdr_wrapper

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab
import os
import telnetlib
import time
import gqrx.gqrx_client

c_sample_rate = 2e6
c_gain = 100
c_number_of_samples = 256*1024

c_start_freq = 91.0e6
c_scanner_delta = int(c_sample_rate / 2)
c_scanner_steps = 1
c_warmup_steps = 3

c_normalize_scan = True
c_diff_scan = True
c_plot_each_step = False

c_gqrx_host = "0.0.0.0"
c_gqrx_port = 7356
c_gqrx_timeout = 100

# Kill GQRX
os.system("pkill gqrx")

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

g_candidates = []

for i in range(c_scanner_steps):

    print()

    target_freq = c_start_freq + i * c_scanner_delta

    samples = sdr_client.scan_freq(
        center_freq=target_freq,
        number_of_samples=c_number_of_samples
    )

    # plt.psd(samples, NFFT=128, Fs=c_sample_rate/1e6, Fc=target_freq/1e6, alpha=.6)
    pxx, frequencies = matplotlib.mlab.psd(samples, NFFT=128, Fs=c_sample_rate/1e6)
    pxx = 10.0*np.log10(pxx)
    frequencies += target_freq/1e6

    if c_normalize_scan:
        # pxx/=np.std(pxx)
        pxx -= np.mean(pxx)

    # Calc and plot threshold
    if c_diff_scan:
        frequencies = frequencies[1:]
        pxx = np.diff(pxx)
    t_mean = np.mean(pxx)
    t_std = np.std(pxx)
    threshold = t_mean + 1.5 * t_std
    plt.hlines(threshold, frequencies[0], frequencies[-1], color='orange', linestyles="dotted")

    # Filter out frequencies greater that threshold
    i_n_targets = np.nonzero(pxx > threshold)[0]

    # Filter out similarly indexes
    print("- Candidates before filtering", len(i_n_targets))
    i_n_targets = np.insert(i_n_targets, 0, 0., axis=0)
    TOL = 1.0
    i = np.argsort(i_n_targets.flat)
    d = np.append(True, np.diff(i_n_targets.flat[i]))
    i_n_targets = i_n_targets.flat[i[d > TOL]]
    print("- Candidates after filtering", len(i_n_targets))

    # Plot these frequencies and add to candidates list
    for i_n in i_n_targets:
        target_freq = frequencies[i_n]
        plt.vlines(target_freq, ymin=np.min(pxx), ymax=np.max(pxx), color='red', linestyles="dotted")
        g_candidates.append(target_freq)

    plt.plot(frequencies, pxx, alpha=0.6)

    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Relative power (dB)')

    if c_plot_each_step:
        plt.show()
        plt.close("all")

if not c_plot_each_step:
    plt.show()

sdr_client.destroy()

print()

# Filter out similarly frequencies
print("- Before duplicate filter", len(g_candidates))
g_candidates = np.array(g_candidates)
TOL = 0.05
i = np.argsort(g_candidates.flat)
d = np.append(True, np.diff(g_candidates.flat[i]))
g_candidates = g_candidates.flat[i[d > TOL]]
print("- After duplicate filter", len(g_candidates))

print()

# Start GQRX
os.system("open -a gqrx")

input("Please open GQRX and start session with remote control.\nPress Enter to continue...")

with telnetlib.Telnet(c_gqrx_host, c_gqrx_port, c_gqrx_timeout) as telnet_session:

    gqrx_client = gqrx.gqrx_client.GqRxClient(telnet_session)

    for candidate_fq in g_candidates:

        gqrx_client.set_freq(candidate_fq * 1e6)
        time.sleep(2)
