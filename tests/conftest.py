import copy

import src.app as app_module


def pytest_configure(config):
    """Ensure the app module is loaded before tests run."""
    return None


import pytest


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original
