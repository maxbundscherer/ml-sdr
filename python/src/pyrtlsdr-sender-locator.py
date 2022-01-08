import pyrtlsdr.pyrtlsdr_wrapper as sdr_wrapper

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab
import os
import telnetlib
import time
import gqrx.gqrx_client
import collections
import scipy.signal

c_tuner_sample_rate = 2e6
c_tuner_gain = 20
c_tuner_num_samples = 256 * 1024

c_scanner_start_freq = 87.0e6
c_scanner_delta = int(c_tuner_sample_rate / 2)
c_scanner_warmup_steps = 5
c_scanner_steps = 8
c_scanner_iterations = 4

c_analyse_psd_nfft = 128
c_analyse_prepare_normalize = False
c_analyse_prepare_diff = False
c_analyse_threshold_std_factor = 2
c_analyse_fg_round_decimals = 4

c_analyse_enable_plot = True
c_analyse_plot_each_step = False

c_analyse_filter_each_scan_enable = False
c_analyse_filter_each_scan_TOL = 1.0  # index value

c_analyse_filter_each_iteration_enable = False
c_analyse_filter_each_iteration_TOL = 0.05  # fq value

c_eval_filter_min_count = 0  # disabled filter
c_eval_filter_max_count = c_scanner_iterations * 100  # disabled filter

c_gqrx_client_enable = True
c_gqrx_client_host = "0.0.0.0"
c_gqrx_client_port = 7356
c_gqrx_client_timeout = 100

# Kill GQRX
if c_gqrx_client_enable:
    os.system("pkill gqrx")

sdr_client = sdr_wrapper.PyRtlSdrWrapper(
    sample_rate=c_tuner_sample_rate,
    gain=c_tuner_gain
)

print()
print("################################################")
print("################ Warum up phase ################")
print("################################################")

for _ in range(c_scanner_warmup_steps):

    print("(Warmup Scan)")
    _ = sdr_client.scan_freq(
        center_freq=c_scanner_start_freq,
        number_of_samples=c_tuner_num_samples
    )

print()
print("################################################")
print("################ Scan phase ####################")
print("################################################")

candidates_global = []

for i_scanner_iteration in range(c_scanner_iterations):

    print()
    print("----------------------------------------")
    print("Scan iteration ", ((i_scanner_iteration + 1) * 100.0 / c_scanner_iterations), "%")
    print("----------------------------------------")

    candidates_per_iteration = []

    for i_scanner_step in range(c_scanner_steps):

        target_freq = c_scanner_start_freq + i_scanner_step * c_scanner_delta

        print()
        samples = sdr_client.scan_freq(
            center_freq=target_freq,
            number_of_samples=c_tuner_num_samples
        )

        # plt.psd(samples, NFFT=128, Fs=c_sample_rate/1e6, Fc=target_freq/1e6, alpha=.6)
        pxx, frequencies = matplotlib.mlab.psd(samples, NFFT=c_analyse_psd_nfft, Fs=c_tuner_sample_rate / 1e6)
        pxx = 10.0*np.log10(pxx)
        frequencies += target_freq/1e6

        if c_analyse_prepare_normalize:
            # pxx/=np.std(pxx)
            pxx -= np.mean(pxx)

        # Calc and plot threshold
        if c_analyse_prepare_diff:
            frequencies = frequencies[1:]
            pxx = np.diff(pxx)
        t_mean = np.mean(pxx)
        t_std = np.std(pxx)
        threshold = t_mean + c_analyse_threshold_std_factor * t_std
        plt.hlines(threshold, frequencies[0], frequencies[-1], color='orange', linestyles="dotted")

        # Filter out frequencies greater that threshold (old way)
        # i_n_targets = np.nonzero(pxx > threshold)[0]

        # Peak finder (new way)
        i_n_targets, _ = scipy.signal.find_peaks(pxx, prominence=1)

        # Filter out similarly indexes
        if c_analyse_filter_each_scan_enable:
            can_before_filter_scan = len(i_n_targets)
            i_n_targets = np.insert(i_n_targets, 0, 0., axis=0)
            i_filter_each_scan = np.argsort(i_n_targets.flat)
            d_filter_each_scan = np.append(True, np.diff(i_n_targets.flat[i_filter_each_scan]))
            i_n_targets = i_n_targets.flat[i_filter_each_scan[d_filter_each_scan > c_analyse_filter_each_scan_TOL]]
            print(" Detected candidates after scan filter", can_before_filter_scan, "from", len(i_n_targets))

        # Plot these frequencies and add to candidates list
        counter_added = 0
        for i_fq in i_n_targets:
            t_target_freq = frequencies[i_fq]
            t_target_db = pxx[i_fq]

            if t_target_db > threshold:
                counter_added = counter_added + 1
                plt.vlines(t_target_freq, ymin=np.min(pxx), ymax=np.max(pxx), color='red', linestyles="dotted")
                candidates_per_iteration.append(t_target_freq.round(decimals=c_analyse_fg_round_decimals))

        print(" Added", counter_added, "from", len(i_n_targets), "candidates (filtered by threshold)")

        if c_analyse_enable_plot:
            plt.plot(frequencies, pxx, alpha=0.6)
            plt.xlabel('Frequency (MHz)')
            plt.ylabel('Relative power (dB)')

        if c_analyse_plot_each_step and c_analyse_enable_plot:
            plt.show()
            plt.close("all")

    if not c_analyse_plot_each_step and c_analyse_enable_plot:
        plt.show()

    plt.close("all")

    # Filter out similarly frequencies
    candidates_per_iteration = np.array(candidates_per_iteration)
    if c_analyse_filter_each_iteration_enable:
        can_before_filter_it = len(candidates_per_iteration)
        i_filter_each_iteration = np.argsort(candidates_per_iteration.flat)
        d_filter_each_iteration = np.append(True, np.diff(candidates_per_iteration.flat[i_filter_each_iteration]))
        g_candidates = candidates_per_iteration.flat[i_filter_each_iteration[d_filter_each_iteration > c_analyse_filter_each_iteration_TOL]]
        print("\nDetected candidates after iteration filter", can_before_filter_it, "from", len(candidates_per_iteration))
    else:
        print("\nDetected candidates in iteration", len(candidates_per_iteration))

    candidates_global.append(candidates_per_iteration)

sdr_client.destroy()

print()
print("################################################")
print("#################### After scan phase ##########")
print("################################################")

print()
print("Got scan iterations", len(candidates_global))
for idx, row in enumerate(candidates_global):
    print("- Candidates by iteration " + str(idx+1) + ":\t", len(row))

candidates_flat_global = []
for lo in candidates_global:
    for li in lo:
        candidates_flat_global.append(li)

print()
print("Got total candidates", len(candidates_flat_global))

candidates_counted = collections.Counter(candidates_flat_global)

print("Got candidates counted", candidates_counted)

plt.bar(candidates_counted.keys(), candidates_counted.values(), width=0.1)
plt.title("Candidates counted (pre filter)")
plt.show()

candidates_gqrx = []

for ret_candidate in candidates_counted:

    if c_eval_filter_min_count <= candidates_counted[ret_candidate] <= c_eval_filter_max_count:
        candidates_gqrx.append(ret_candidate)

candidates_gqrx.sort()

candidates_counted_gqrx = collections.Counter(candidates_gqrx)

plt.bar(candidates_counted_gqrx.keys(), candidates_counted_gqrx.values(), width=0.1)
plt.title("Candidates counted (after filter)")
plt.show()

print("Got candidates after counter filter", len(candidates_gqrx), "(filter from " + str(c_eval_filter_min_count) + " to " + str(c_eval_filter_max_count) + ")")

print("RAW", candidates_gqrx)

if c_gqrx_client_enable:

    # Start GQRX
    os.system("open -a gqrx")

    print()
    input("Please open GQRX and start session with remote control.\nPress Enter to continue...")

    with telnetlib.Telnet(c_gqrx_client_host, c_gqrx_client_port, c_gqrx_client_timeout) as telnet_session:

        gqrx_client = gqrx.gqrx_client.GqRxClient(telnet_session)

        while True:

            for candidate_fq in candidates_gqrx:

                gqrx_client.set_freq(candidate_fq * 1e6)
                print("- Counted", candidates_counted[candidate_fq])
                time.sleep(2)
                print()
