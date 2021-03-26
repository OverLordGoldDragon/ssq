import pytest

def test_main():
    assert 1 + 1 == 2

if __name__ == '__main__':
    pytest.main([__file__, "-s"])
