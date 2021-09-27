import random

from factory import Factory, Faker, fuzzy

from planner.planning import Task

fake = Faker._get_faker()
AVAILABLE_RESOURCES = 6
ALL_RESOURCES = [fake.word() for _ in range(AVAILABLE_RESOURCES)]


def get_random_resources():
    n_resources = random.randint(1, AVAILABLE_RESOURCES)
    return random.sample(ALL_RESOURCES, n_resources)


class TasksFactory(Factory):

    class Meta:
        model = Task

    name = Faker('word')
    payoff = Faker('pyfloat', min_value=0.0, max_value=10.0)
    resources = fuzzy.FuzzyAttribute(get_random_resources)
