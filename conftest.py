import pytest
from app import App


@pytest.fixture(scope='module')
def app():
    """Creates App fixture"""
    app = App()
    return app
