import pytest


@pytest.fixture(autouse=True)
def clean_text_file():
    with open("tests/testfile.txt", "r"):
        pass
