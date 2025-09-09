import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def disable_toolbar_in_tests(monkeypatch):
    monkeypatch.setattr(settings, "DEBUG", True)
