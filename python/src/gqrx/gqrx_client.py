class GqRxClient:

    def __init__(self, telnet_session):
        self.telnet_session = telnet_session

    ##################################################
    ## Mods ##########################################
    ##################################################

    def set_mod_wfm_stereo(self):
        print("- Set mod to WFM Stereo")
        self.telnet_session.write(b"M WFM_ST\n")

    def set_mod_wfm_mono(self):
        print("- Set mod to WFM Mono")
        self.telnet_session.write(b"M WFM\n")

    def set_mod_nfm(self):
        print("- Set mod to Narrow FM")
        self.telnet_session.write(b"M FM\n")

    def set_mod_am(self):
        print("- Set mod to AM")
        self.telnet_session.write(b"M AM\n")

    def set_mod_lsb(self):
        print("- Set mod to LSB")
        self.telnet_session.write(b"M LSB\n")

    def set_mod_usb(self):
        print("- Set mod to USB")
        self.telnet_session.write(b"M USB\n")

    def set_mod_cw_l(self):
        print("- Set mod to CW-L")
        self.telnet_session.write(b"M CWL\n")

    def set_mod_cw_u(self):
        print("- Set mod to CW-U")
        self.telnet_session.write(b"M CWU\n")

    def set_mod_raw_iq(self):
        print("- Set mod to RAW-IQ")
        self.telnet_session.write(b"M RAW\n")

    ##################################################
    ## Freq ##########################################
    ##################################################

    def set_freq(self, freq):
        print("- Set freq to", freq)
        self.telnet_session.write(str.encode("F " + str(freq) + "\n"))