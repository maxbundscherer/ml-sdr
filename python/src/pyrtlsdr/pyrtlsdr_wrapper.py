import rtlsdr


class PyRtlSdrWrapper:

    def __init__(self, sample_rate, gain):
        self.sdr = rtlsdr.RtlSdr()
        self.sdr.sample_rate = sample_rate
        # self.sdr.bandwidth = bandwidth
        self.sdr.gain = gain

    def scan_freq(self, center_freq, number_of_samples):
        print("- Scan now", center_freq/1e6, "MHz")
        self.sdr.center_freq = center_freq
        return self.sdr.read_samples(number_of_samples)

    def destroy(self):
        self.sdr.close()
