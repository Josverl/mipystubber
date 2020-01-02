#!/usr/bin/env python3
"""
Collect modules and python stubs from MicroPython source projects
"""
# Copyright (c) 2020 Jos Verlinde
# MIT license
# some functions used from makemanifest.py,
#   part of the MicroPython project, http://micropython.org/
#   Copyright (c) 2019 Damien P. George

import glob
import os
import re
import shutil

path_vars = {"MPY_DIR":"", "MPY_LIB_DIR":"", "PORT_DIR":"", "BOARD_DIR":""}
stub_dir = None

# functions from makemanifest to ensure that the manifest.py files can be processed
class FreezeError(Exception):
    pass

# freeze_as_mpy is only used by the unix port.
def freeze_as_mpy(path, script=None, opt=0):
    freeze(path, script, opt)

# function used commenly in manifest.py to freeze a set of scripts
# pylint: disable=unused-argument
def freeze(path, script=None, opt=0):
    """Freeze the input, automatically determining its type.  A .py script
    will be compiled to a .mpy first then frozen, and a .mpy file will be
    frozen directly.

    `path` must be a directory, which is the base directory to search for
    files from.  When importing the resulting frozen modules, the name of
    the module will start after `path`, ie `path` is excluded from the
    module name.

    If `path` is relative, it is resolved to the current manifest.py.
    Use $(MPY_DIR), $(MPY_LIB_DIR), $(PORT_DIR), $(BOARD_DIR) if you need
    to access specific paths.

    If `script` is None all files in `path` will be frozen.

    If `script` is an iterable then freeze() is called on all items of the
    iterable (with the same `path` and `opt` passed through).

    If `script` is a string then it specifies the filename to freeze, and
    can include extra directories before the file.  The file will be
    searched for in `path`.

    `opt` is the optimisation level to pass to mpy-cross when compiling .py
    to .mpy. (ignored in this implementation)
    """
    path = convert_path(path)
    if script is None:
        #folder of scripts.
        for s in os.listdir(path):
            freezedry(path, s)

        # for dirpath, dirnames, filenames in os.walk(path, followlinks=True):
        #     for f in filenames:
        #         freeze_internal(kind, path, (dirpath + '/' + f)[len(path) + 1:], opt)
    elif not isinstance(script, str):
        # several specific scripts.
        for s in script:
            freezedry(path, s)
    else:
        # on specific script.
        freezedry(path, script)

# called by freeze.
def freezedry(path, script, dirpath=None):
    "copy the to-be-frozen module to the desination folder to be stubbed"
    script_path = os.path.join( path, script)
    if stub_dir:
        print("freezedry : {:<20} to {}".format(script, stub_dir))
        # ensure folder
        if not os.path.exists(stub_dir):
            os.makedirs(stub_dir, exist_ok=True)
        # copy file
        try:
            shutil.copy2(script_path, stub_dir)
        except OSError as e:
            print(e)
    else:
        print('Stub folder not set')

def include(manifest):
    """Include another manifest.

    The manifest argument can be a string (filename) or an iterable of
    strings.

    Relative paths are resolved with respect to the current manifest file.
    """
    if not isinstance(manifest, str):
        for m in manifest:
            include(m)
    else:
        manifest = convert_path(manifest)
        with open(manifest) as f:
            # Make paths relative to this manifest file while processing it.
            # Applies to includes and input files.
            prev_cwd = os.getcwd()
            os.chdir(os.path.dirname(manifest))
            exec(f.read())  # pylint: disable=exec-used
            os.chdir(prev_cwd)

def convert_path(path):
    "Perform variable substituion in path"
    for name, value in path_vars.items():
        path = path.replace('$({})'.format(name), value)
    # Convert to absolute path (so that future operations don't rely on
    # still being chdir'ed).
    return os.path.abspath(path)

def get_frozen(stub_path, mpy_path=None, lib_path=None):
    """
    get and parse the to-be-fozen .py modules for micropython to extract the static type information
    - requires that the MicroPython and Micropython-lib repos are checked out and available on a local path
      repos should be cloned side-by-side as some of the manifests refer to micropython-lib scripts using a relative path
    """
    global path_vars # pylint: disable=global-statement
    global stub_dir  # pylint: disable=global-statement

    if not mpy_path:
        mpy_path = '..\\micropython'
    if not lib_path:
        lib_path = '..\\micropython-lib'
    if not stub_path:
        stub_path = './stubs/mpy_1_12/frozen'
    # get the manifests of the different ports and boards
    mpy_path = os.path.abspath(mpy_path)
    lib_path = os.path.abspath(lib_path)
    stub_path = os.path.abspath(stub_path)

    path_vars['MPY_DIR'] = mpy_path
    path_vars['MPY_LIB_DIR'] = lib_path

    # manifest.py is used for board specifican and daily builds
    # manifest_release.py is used for the release builds
    manifests = glob.glob(mpy_path + '\\ports\\**\\manifest.py', recursive=True) + glob.glob(mpy_path + '\\ports\\**\\manifest_release.py', recursive=True)

    # https://regexr.com/4rh39
    # but with an extry P for Python named groups...
    regex_2 = r"(?P<board>(?P<port>.*[\\/]+ports[\\/]+\w+)[\\/]+boards[\\/]+\w+)"   # port & board
    regex_1 = r"(?P<port>.*[\\/]+ports[\\/]+\w+)[\\/]+boards[\\/]+\w+"              # port
    # matches= re.search(regex, 'C:\\develop\\MyPython\\micropython\\ports\\esp32\\boards\\TINYPICO\\manifest.py')
    # print( matches.group('port'), matches.group('board'))

    # Include top-level inputs, to generate the manifest
    for manifest in manifests:
        print('Manifest:', manifest)
        matches = re.search(regex_2, manifest)
        path_vars['PORT_DIR'] = ""
        path_vars['BOARD_DIR'] = ""
        if matches:
            # port and board
            path_vars['PORT_DIR'] = matches.group('port') or ""
            path_vars['BOARD_DIR'] = matches.group('board') or ""
            if os.path.basename(matches.group('board')) == "manifest":
                path_vars['BOARD_DIR'] = ""
        else:
            #just port
            matches = re.search(regex_1, manifest)
            if matches:
                path_vars['PORT_DIR'] = matches.group('port') or ""

        port_name = os.path.basename(path_vars['PORT_DIR'])
        board_name = os.path.basename(path_vars['BOARD_DIR'])

        if board_name == "":
                board_name = "GENERIC"

        if board_name == "manifest_release":
                board_name = "RELEASE"
        
        # set global for later use - must be an absolute path.
        stub_dir = os.path.abspath(os.path.join(stub_path, port_name, board_name))

        try:
            include(manifest)
        except FreezeError as er:
            print('freeze error executing "{}": {}'.format(manifest, er.args[0]))


if __name__ == "__main__":
    # MicroPython
    # todo: checkout micropython @ tag
    get_frozen(stub_path='./stubs/mpy_1_12/frozen', mpy_path='../micropython', lib_path='../micropython-lib')

    # PyCopy / LoBo - do not use manifests
    # modules are in directly in the PORT/modules folder
    # get_frozen_MP(stub_path='./stubs/pycopy/frozen', mpy_path= '../pycopy', lib_path= '../pycopy-lib')
