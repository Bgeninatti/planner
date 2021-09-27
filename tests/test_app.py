from pathlib import Path

import pytest

from planner.app import application

SAMPLE_TASKS = Path(__file__).parent / "sample_tasks"


class TestIndex:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = application.test_client()

    @pytest.fixture()
    def tasks_file(self):
        with open(SAMPLE_TASKS / 'problem_statement_tasks.json', 'rb') as f:
            yield {'tasks-file': (f, 'tasks.json')}

    @pytest.fixture()
    def bad_tasks_file(self):
        with open(SAMPLE_TASKS / 'bad_tasks_file.json', 'rb') as f:
            yield {'tasks-file': (f, 'tasks.json')}

    def test_get_index(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_post(self, tasks_file):
        response = self.client.post('/', data=tasks_file)
        assert response.status_code == 200

    def test_post_wrong_file(self, bad_tasks_file):
        response = self.client.post('/', data=bad_tasks_file)
        assert response.status_code == 400
