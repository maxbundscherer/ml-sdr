# ML SDR

Just another approach to do machine learning stuff on software defined radio.

``rtl - sdr - gqrx - pyrtlsdr - python - machine learning``

[![shields.io](https://img.shields.io/badge/license-Apache2-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)

Author: [Maximilian Bundscherer](https://bundscherer-online.de)

## Overview

![](./doc-img/sdr.png)

*GQRX sample*

![](./doc-img/pyrtlsdr-2d.png)

*Included 2d scanner*

![](./doc-img/pyrtlsdr-3d.png)

*Included 3d scanner*

### Features

- **Mode 1**: Python sdr scanner controller ([gqrx](https://gqrx.dk/) client)
- **Mode 2**: Python sdr experiments (2d and 3d scanner) ([pyrtlsdr](https://pyrtlsdr.readthedocs.io/en/latest/) api)

### Requirements

- [GQRX](https://gqrx.dk/) (only mode 1)
- Python (pip requirements included) (3.9 recommend)

### Mode 1 (Gqrx Sdr Client)

- Create virtual python env
- Install requirements (see script in ``python/``)
- Enable remote control in gqrx
    - Set port ``7356``
    - Add ``localhost``, ``0.0.0.0`` to allowed hosts
- Run python file in ``python/src/gqrx-sdr-scanner.py``

### Mode 2 (pyrtlsdr)

- Create virtual python env
- Install requirements (see script in ``python/``)
- **2D Scan**: Run python file in ``python/src/pyrtlsdr-2d-scanner.py``
- **3D Scan**: Run python file in ``python/src/pyrtlsdr-3d-scanner.py``
