#!/usr/bin/env python3
"""
Collect modules and python stubs from the Loboris MicroPython source project
"""
# pylint: disable= line-too-long
# Copyright (c) 2020 Jos Verlinde
# MIT license
import logging
from pathlib import Path
import downloader
import utils

FAMILY = 'loboris'
fmly = 'lobo'
PORT = 'esp32_lobo'


log = logging.getLogger(__name__)
# log.setLevel(level=logging.DEBUG)

def get_frozen(stub_path=None, *, repo=None, version='3.2.24'):
    "Loboris frozen modules"
    if not stub_path:
        stub_path = Path('./all-stubs')  / "{}-{}-frozen".format(FAMILY, utils.flat_version(version) )
    else:
        stub_path = Path(stub_path)

    if not repo:
        repo = 'https://raw.githubusercontent.com/loboris/MicroPython_ESP32_psRAM_LoBo/master/MicroPython_BUILD/components/micropython/esp32/modules/{}'

    frozen_modules = ["README.md", "ak8963.py", "freesans20.py", "functools.py", "logging.py", "microWebSocket.py", "microWebSrv.py", "microWebTemplate.py", "mpu6500.py", "mpu9250.py", "pye.py", "ssd1306.py", "tpcalib.py", "upip.py",
                      "upip_utarfile.py", "upysh.py", "urequests.py", "writer.py"]
    #download
    downloader.download_files(repo, frozen_modules, stub_path)
    # make a manifest 
    utils.make_manifest(stub_path, FAMILY, "frozen", fmly, version=version)


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)-8s:%(message)s',level=logging.INFO)
    get_frozen(version='3.2.24')
