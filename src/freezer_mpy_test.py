import pytest
import os
import basicgit as git
#SOT 
import freezer_mpy

# No Mocks, does actual extraction from repro 
# todo: get seperate test instaNCE OF THE REPO 

def test_freezer_mpy(tmp_path):
    mpy_path = '../micropython' 

    version = git.get_tag(mpy_path)
    if version < 'v1.12':
        git.checkout_tag('v1.12',mpy_path)

    assert version >= 'v1.12', ""
    # mpy version must be at 1.12 or newer 

    stub_path = tmp_path
    freezer_mpy.get_frozen(stub_path, mpy_path, lib_path='../micropython-lib') 
    assert True

    #assert len(list(tmp_path.iterdir())) == 18, "there should be 18 files"




