import pytest
import os

#SOT
import downloader
#SOT 2
import freezer_lobo

# No Mocks , does actual download from github


def test_download_files(tmp_path):
    repo = 'https://raw.githubusercontent.com/loboris/MicroPython_ESP32_psRAM_LoBo/master/MicroPython_BUILD/components/micropython/esp32/modules/{}'

    frozen_modules = ["README.md", "ak8963.py"]
    #download
    downloader.download_files(repo, frozen_modules, tmp_path)
    assert len(list(tmp_path.iterdir())) == 2, "there should be 2 files"
    for file in frozen_modules:
        fname = os.path.join(tmp_path, file)
        assert os.path.exists( fname ), "file {} is downloaded".format(file)

def test_freezer_lobo(tmp_path):
    freezer_lobo.get_frozen(tmp_path)
    assert len(list(tmp_path.iterdir())) == 18, "there should be 18 files"

