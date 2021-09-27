from itertools import chain

import pytest
from tests.factories import TasksFactory

from planner.planning import ActionPlan, ActionPlanSelector, DomainBuilder


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


class TestDomainBuilder:

    @staticmethod
    def is_plan_possible(plan):
        all_resources = list(chain(*(t.resources for t in plan.tasks)))
        return len(plan.required_resources) == len(all_resources)

    @pytest.fixture()
    def tasks(self):
        return TasksFactory.build_batch(5)

    @pytest.fixture()
    def full_tree(self, tasks):
        domain = [ActionPlan(tasks=[t]) for t in tasks]
        for node in domain:
            candidate_tasks = filter(lambda t: t not in node.tasks, tasks)
            for task in candidate_tasks:
                new_node = ActionPlan(tasks=node.tasks + [task])
                domain.append(new_node)
        return domain

    @pytest.fixture()
    def possible_plans(self, full_tree):
        return [node for node in full_tree if self.is_plan_possible(node)]

    @pytest.fixture()
    def domain(self, tasks):
        build_domain = DomainBuilder()
        return build_domain(tasks)

    def test_domain_exclude_imposible_action_plans(self, possible_plans, domain):
        assert len(possible_plans) == len(domain)
        for node in domain:
            assert self.is_plan_possible(node)


class TestActionPlanSelector:

    @pytest.fixture(autouse=True)
    def setup(self, mocker, domain):
        mocker.patch(
            'planner.planning.DomainBuilder.__call__',
            return_value=domain
        )
        self.select_action_plan = ActionPlanSelector()

    @pytest.fixture()
    def domain(self):
        return [
            ActionPlan(tasks=TasksFactory.build_batch(2, payoff=100)),
            ActionPlan(tasks=TasksFactory.build_batch(2, payoff=1))
        ]

    @pytest.fixture()
    def tasks(self):
        return TasksFactory.build_batch(5)

    def test_selects_higher_reward_action_plan(self, tasks):
        action_plan = self.select_action_plan(tasks)
        assert action_plan.reward == 200
