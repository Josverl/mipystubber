# run createsubs in the unix version of micropython
import os
import json
import subprocess
from pathlib import Path
import pytest

#  ROOT = Path(__file__).parent

@pytest.mark.parametrize(
    "script_folder", [ ('./board') , ('./minified') ]
)

@pytest.mark.parametrize(
    "firmware", [ ('micropython_1_12') , ('micropython_1_13'), ('pycopy_3_3_2-25') ]
)


def test_createstubs(firmware, tmp_path, script_folder):
    # run createsubs in the unix version of micropython
    # Use temp_path to generate stubs 
    scriptfolder = os.path.abspath(script_folder)
    cmd = [os.path.abspath('tools/'+firmware), 'createstubs.py', '--path', tmp_path]
    try:
        subproc = subprocess.run(cmd,cwd=scriptfolder, timeout=100000)
        assert (subproc.returncode == 0 ), "createstubs ran with an error"
        # assert (subproc.returncode <= 0 ), "createstubs ran with an error"
    except ImportError:
        pass
    # did it run without error ?

    stubfolder = Path(tmp_path)  / 'stubs'
    stubfiles = list(stubfolder.rglob('*.py'))
    # filecount 
    if 'micropython' in script_folder:
        assert (len(stubfiles) >= 45 ), "micropython: there should be 45 stubs or more"
    else:
        assert (len(stubfiles) >= 30 ), "pycopy: there should be 30 stubs or more"

    # manifest exists
    jsons = list(stubfolder.rglob('modules.json'))
    assert (len(jsons) == 1 ), "there should be 1 manifest"

    # manifest is valid json
    # read file
    manifest = None
    with open(jsons[0], 'r') as file:
        manifest=json.load(file)

    assert (len(manifest) == 3 ), "module manifest should contain firmware, stubber , modules"

    assert (len(manifest['modules']) == len(stubfiles) ), "number of modules must match count of stubfiles"
