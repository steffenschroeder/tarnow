import pytest
import os

@pytest.fixture(autouse=True)
def change_tempory_directory(tmpdir):
    tmpdir.chdir()
    yield
    if os.path.exists("tarnow.tmp"):
        os.remove("tarnow.tmp")


@pytest.fixture(autouse=True)
def patch_subprocess(mocker):
    mocker.patch('subprocess.call')
