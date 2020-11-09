#SOT
import pytest
import utils


@pytest.mark.parametrize(
    "commit, build, clean",
    [   
        ('v1.13-103-gb137d064e', True, 'v1.13-103'),
        ('v1.13-103-gb137d064e', False, 'v1.13-N'),

        ('v1.13', True, 'v1.13'),
        ('v1.13', False, 'v1.13'),

# #BUG:?
        ('v1.13-dirty', True, 'v1.13'),
        ('v1.13-dirty', False, 'v1.13-N'),

    ]
)

def test_clean_version(commit, build, clean):
    assert utils.clean_version(commit, build) == clean

# test manifest()


# make manifest 
