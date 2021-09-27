from itertools import chain

import pytest
from tests.factories import TasksFactory

from planner.planning import ActionPlan


class TestActionPlan:

    @pytest.fixture()
    def tasks(self):
        return TasksFactory.build_batch(10)

    @pytest.fixture()
    def action_plan(self, tasks):
        return ActionPlan(tasks=tasks)

    @pytest.fixture()
    def imposible_task(self, action_plan):
        return TasksFactory(resources=action_plan.required_resources)

    @pytest.fixture()
    def another_task(self):
        return TasksFactory()

    def test_reward(self, action_plan, tasks):
        assert action_plan.reward == sum(t.payoff for t in tasks)

    def test_required_resources(self, action_plan, tasks):
        all_resources = list(chain(*(t.resources for t in tasks)))
        assert all(r in action_plan.required_resources for r in all_resources)

    def test_add_task_include_task(self, action_plan, another_task):
        assert another_task not in action_plan.tasks
        action_plan.add_task(another_task)
        assert another_task in action_plan.tasks

    def test_add_task_increase_reward(self, action_plan, another_task):
        previous_reward = action_plan.reward
        action_plan.add_task(another_task)
        assert action_plan.reward == previous_reward + another_task.payoff

    def test_can_include(self, action_plan, imposible_task):
        assert not action_plan.can_include(imposible_task)
