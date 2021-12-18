# ML SDR

Just another approach to do machine learning stuff on software defined radio.

``sdr - machine learning``

[![shields.io](https://img.shields.io/badge/license-Apache2-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)

Author: [Maximilian Bundscherer](https://bundscherer-online.de)

## Overview

![](./doc-img/sdr.png)

### Features

- Python sdr scanner (gqrx client)
- tbd (work in progress)

### Requirements

- [GQRX](https://gqrx.dk/)
- Python (pip requirments included) (3.9 recommend)

### Let's get started (Gqrx Sdr Client)

- Create virutal python env
- Install requirements (see script in ``python/``)
- Enable remote control in gqrx
    - Set port ``7356``
    - Add ``localhost``, ``0.0.0.0`` to allowed hosts
- Run python-scripts in ``python/src/``
