from typing import Callable, List, Set

import attr


@attr.s
class Task:
    name: str = attr.ib()
    payoff: float = attr.ib()
    resources: Set[str] = attr.ib(converter=set)


@attr.s
class ActionPlan:
    tasks: List[Task] = attr.ib()
    reward: float = attr.ib(init=False, default=0.0)
    required_resources: Set[str] = attr.ib(init=False, default=set)

    def __attrs_post_init__(self):
        self.required_resources = set.union(*(t.resources for t in self.tasks))
        self.reward = sum(t.payoff for t in self.tasks)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.reward += task.payoff
        self.required_resources = self.required_resources.union(task.resources)

    def can_include(self, task: Task) -> bool:
        return not self.required_resources.intersection(task.resources)


class DomainBuilder:

    def __call__(self, tasks: List[Task]) -> List[ActionPlan]:
        resources_count = len(ActionPlan(tasks=tasks).required_resources)  # Compute how many unique resources are
        domain = [ActionPlan(tasks=[t]) for t in tasks]
        for node in domain:
            if len(node.required_resources) == resources_count:
                # There is no available resources in the action plan.
                continue
            # Attempt to add additional tasks into the action plan
            candidate_tasks = filter(lambda t: node.can_include(t), tasks)
            for task in candidate_tasks:
                new_node = ActionPlan(tasks=node.tasks + [task])
                domain.append(new_node)
        return domain


class ActionPlanSelector:

    _build_domain: Callable = DomainBuilder()

    def __call__(self, tasks: List[Task]) -> ActionPlan:
        domain = self._build_domain(tasks)
        domain.sort(key=lambda m: m.reward)
        winner = domain.pop()
        return winner
