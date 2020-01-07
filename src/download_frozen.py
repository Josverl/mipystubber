#!/usr/bin/env python3
"""
Collect modules and python stubs from other projects
"""
# Copyright (c) 2020 Jos Verlinde
# MIT license

import glob
import os
import shutil
import subprocess

import basicgit as git
import freezer_mpy
import freezer_lobo

# todo: add frozen modules for :
# import freezer_pycopy
# import freezer_pycom

def make_stub_files(stub_path, levels: int = 1):
    "generate typeshed files for all scripts in a folder"
    # TODO: do this nicer by loading the module

    level = ""
    # make_sub_files.py only does one folder level at a time
    # so lets try 7 levels /** ,  /**/** , etc
    for i in range(levels):
        cmd = "py ./src/make_stub_files.py -c ./src/make_stub_files.cfg -u {}{}/*.py".format(stub_path, level)
        print("level {} : {}".format(i+1, cmd))
        os.system(cmd)
        level = level + '/**'


def get_frozen_pyb(stub_path):
    # pyboard custom stub is included and does not need to be downloaded.
    stub_path = './stubs/pyb_common'
    ## modules = ['pyb.py']
    ## url = 'https://raw.githubusercontent.com/dastultz/micropython-pyb/master/lib/{}'
    ## download_files(url, modules,  savepath )

#def pip_download(requirements, path:str):
def get_cpython(requirements, stub_path=None):
    "Download MicroPython compatibility modules"
    if not stub_path:
        stub_path = './stubs/cpython-core'
    # use pip to dowload requirements file to build folder in one go
    #   pip install --no-compile --no-cache-dir --target ./scratch/test --upgrade -r ./src/microcpython.txt
    build_path = os.path.abspath("./build")
    os.makedirs(stub_path, exist_ok=True)
    os.makedirs(build_path, exist_ok=True)
    try:
        subprocess.run(["pip", "install", "--target", build_path, "-r", requirements, "--no-cache-dir", "--no-compile", "--upgrade"], capture_output=False, check=True)
        # copy *.py files in build folder to stub_path
        for filename in glob.glob(os.path.join(build_path, "*.py")):
            print("pipped :", filename)
            try:
                shutil.copy2(filename, stub_path)
            except OSError as e:
                print(e)
    except:
        print("An error occurred while trying to run pip to dowload the MicroPython compatibility modules from PyPi")
    finally:
        # remove build folder
        shutil.rmtree(build_path, ignore_errors=True)


def flat_version(version: str):
    "Turn 'v1.2.3' into '1_2_3' "
    return version.replace('v', '').replace('.', '_')


def do_all():
    #todo: checkout/check specific version of micropython
    mpy_path = '../micropython'
    version = git.get_tag(mpy_path)
    if version:
        stub_path = './stubs/mpy_{}_frozen'.format(flat_version(version))
        freezer_mpy.get_frozen(stub_path, mpy_path, lib_path='../micropython-lib')
        make_stub_files(stub_path, levels=7)


    # get_cpython(stub_path='./stubs/cpython-core', requirements='./src/micro-cpython.txt')

    # # get_frozen_pyb()

    # freezer_lobo.get_frozen(stub_path='./stubs/esp32_LoBo_3_2_24_Frozen')

    # # now generate typeshed files for all scripts
    # make_stub_files('./stubs', levels=7)



if __name__ == "__main__":
    do_all()
    # get_cpython(stub_path='./stubs/cpython-core', requirements='./src/micro-cpython.txt')
