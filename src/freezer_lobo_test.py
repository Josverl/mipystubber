import pytest
import os

#SOT 
import freezer_lobo

# No Mocks, does actual download from github

def test_freezer_lobo(tmp_path):
    freezer_lobo.get_frozen(tmp_path)
    assert len(list(tmp_path.iterdir())) == 18, "there should be 18 files"




