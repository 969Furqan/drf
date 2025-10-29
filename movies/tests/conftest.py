import pytest

@pytest.fixture(autouse=True)
def enable_eager_tasks(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True