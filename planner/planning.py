from typing import List, Set

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
