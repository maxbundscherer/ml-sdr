import pyrtlsdr.pyrtlsdr_wrapper as sdr_wrapper

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.mlab

c_sample_rate = 2e6
c_gain = 100
c_number_of_samples = 1*1024 ## TODO: Check - added for quick scan

c_start_freq = 91.0e6
c_scanner_delta = int(c_sample_rate / 2)
c_scanner_steps = 9
c_normalize_scan = True

c_time_steps = 100
c_warmup_steps = 10

sdr_client = sdr_wrapper.PyRtlSdrWrapper(
    sample_rate=c_sample_rate,
    gain=c_gain
)

df_ret = pd.DataFrame()

iteration = 0

for i_time_step in range(c_time_steps):

    print()
    print("Scanning...", i_time_step+1, "from", c_time_steps)

    for i_scan_step in range(c_scanner_steps):

        target_freq = c_start_freq + i_scan_step * c_scanner_delta

        samples = sdr_client.scan_freq(
            center_freq=target_freq,
            number_of_samples=c_number_of_samples
        )

        pxx, frequencies = matplotlib.mlab.psd(samples, NFFT=64, Fs=c_sample_rate/1e6)
        pxx = 10.0*np.log10(pxx)
        frequencies += target_freq/1e6

        if c_normalize_scan:
            # pxx/=np.std(pxx)
            pxx -= np.mean(pxx)

        # Modify for plot
        pxx = (pxx/10)-100
        t = float(i_time_step + (i_scan_step / c_scanner_steps))

        if iteration >= c_warmup_steps:
            df_t = pd.DataFrame({"freq": frequencies, "pxx": pxx, "t": t})
            df_ret = df_ret.append(df_t)
        else:
            print("(Warmup phase)")

        iteration = iteration + 1

sdr_client.destroy()

fig = go.Figure(data=[go.Scatter3d(
    x=df_ret["t"],
    y=df_ret["freq"],
    z=df_ret["pxx"],
    mode='markers',
    marker=dict(
        size=10,
        symbol='cross',
        color=df_ret["pxx"],
        colorscale='Inferno'
    )
)])

fig.show()
