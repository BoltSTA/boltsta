import boltsta


def test_read_liberty():
    lib = boltsta.readers.read_liberty("example.lib")
    assert lib.name == "example"
