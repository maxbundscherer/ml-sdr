import gqrx.gqrx_client

import telnetlib
import time

c_host = "0.0.0.0"
c_port = 7356
c_timeout = 100

def default_wait():
    time.sleep(0.2)

with telnetlib.Telnet(c_host, c_port, c_timeout) as telnet_session:

    gqrx_client = gqrx.gqrx_client.GqRxClient(telnet_session)

    gqrx_client.set_mod_usb()
    default_wait()

    for i in range(100):

        start_freq = 7000000
        factor_skip = 1000

        target_freq = i * factor_skip + start_freq

        gqrx_client.set_freq(target_freq)
        default_wait()
