import pytest
# Connects our tests with our database
pytestmark = pytest.mark.django_db

from everycheese.cheeses.models import Cheese
from everycheese.cheeses.tests.factories import CheeseFactory


def test__str__():
    cheese = CheeseFactory()
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name
