import pytest

#SOT
import basicgit as git

def common_tst(tag):
    print(tag)
    assert isinstance(tag, str), "tag must be a string"
    assert tag.startswith('v'), "tags start with a v"
    assert len(tag) >= 2, "tags are longer than 2 chars"

def test_get_tag_current():
    import os
    if not os.path.exists('.git'):
        pytest.skip("no git repo in current folder")
    else:
        # get tag of current repro
        common_tst(git.get_tag())

        for testcase in ['.', '.git', './.git', '.\\.git']:
            common_tst(git.get_tag(testcase))

def test_get_tag_sibling():
    # get version of sibling repro
    for testcase in ['../micropython', '..\\micropython']:
        common_tst(git.get_tag(testcase))

def test_get_failure_throws():
    with pytest.raises(Exception):
        git.get_tag('.not')

def test_checkout_sibling():
    x = git.get_tag('../micropython') 

    for ver in ['v1.11', 'v1.9.4' ,'v1.12']:
        git.checkout_tag(ver, repo='../micropython')  
        assert git.get_tag('../micropython') == ver

    git.checkout_tag(x, repo='../micropython')
    assert git.get_tag('../micropython') == x, "can restore to prior version"

