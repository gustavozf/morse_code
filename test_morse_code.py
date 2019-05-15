import pytest
from morse_code.app import *

def test_valid_input_file():
    assert main(['app.py', 'code.morse']), "Test Failed!"
    assert main(['app.py', 'audio.wav']),  "Test Failed!"
    assert main(['app.py', 'text.txt']),   "Test Failed!"

def test_invalid_input_file():
    assert not main(['app.py']),             "Test Failed!"
    assert not main(['app.py', 'file.wv']),  "Test Failed!"
    assert not main(['app.py', 'file']),     "Test Failed!"
    assert not main(['app.py', 'file.']),    "Test Failed!"