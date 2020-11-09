import os
import glob
import shutil
import subprocess
import logging
import json

import utils
from version import VERSION

log = logging.getLogger(__name__)

family = 'common'

def get_core(requirements, stub_path=None):
    "Download MicroPython compatibility modules"
    if not stub_path:
        stub_path = './all-stubs/cpython-core'

    # use pip to dowload requirements file to build folder in one go
    #   pip install --no-compile --no-cache-dir --target ./scratch/test --upgrade -r ./src/micropython.txt
    build_path = os.path.abspath("./build")
    os.makedirs(stub_path, exist_ok=True)
    os.makedirs(build_path, exist_ok=True)
    mod_manifest = None
    try:
        subprocess.run(["pip", "install", "--target", build_path, "-r", requirements,
                        "--no-cache-dir", "--no-compile", "--upgrade", "--no-binary=:all:"],
                       capture_output=False, check=True)
        # build modules.json
        mod_manifest = utils.manifest(machine=family, version=VERSION)
        # copy *.py files in build folder to stub_path
        for filename in glob.glob(os.path.join(build_path, "*.py")):
            log.info("pipped : {}".format(filename))
            f_name, f_ext = os.path.splitext(os.path.basename(filename)) #pylint: disable=unused-variable
            mod_manifest['modules'].append({"file": os.path.basename(filename), "module":f_name})
            try:
                shutil.copy2(filename, stub_path)
            except OSError as err:
                log.exception(err)
    except OSError as err:
        log.error("An error occurred while trying to run pip to dowload the MicroPython compatibility modules from PyPi: {}".format(err))
    finally:
        # remove build folder
        shutil.rmtree(build_path, ignore_errors=True)
        if mod_manifest:
            #write the the module manifest
            with open(stub_path+"/modules.json", "w") as outfile:
                json.dump(mod_manifest, outfile)

if __name__ == "__main__":
    # just run a quick test
    logging.basicConfig(format='%(levelname)-8s:%(message)s', level=logging.INFO)
    get_core(requirements='./src/reqs-cpython-mpy.txt', stub_path='./scratch/cpython_common')
