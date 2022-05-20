import os
from pickle import TRUE
import tempfile

import pytest

from web_interface.web_interface import app as flask_app

@pytest.fixture
def app():
    app.config['TESTING'] =True
    app.testing = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()