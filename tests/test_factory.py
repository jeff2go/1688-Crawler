import pytest

from app import create_app


@pytest.mark.fast
def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


@pytest.mark.fast
def test_index(client):
    response = client.get('/')
    assert b'1688' in response.data
