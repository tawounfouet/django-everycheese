import pytest
from django.test import RequestFactory
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from everycheese.users.models import User
from everycheese.users.views import (
    UserRedirectView,
    UserUpdateView,
)

from everycheese.users.tests.factories import UserFactory

@pytest.fixture
def user():
    return UserFactory()



pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(
        self, user: User, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(
        self, user: User, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_form_valid(
        self, user: User, request_factory: RequestFactory
    ):
        form_data = {"name": "John Doe"}
        request = request_factory.post(
            reverse("users:update"), form_data
        )
        request.user = user
        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        msg_middleware = MessageMiddleware()
        msg_middleware.process_request(request)

        response = UserUpdateView.as_view()(request)
        user.refresh_from_db()

        assert response.status_code == 302
        assert user.name == form_data["name"]


class TestUserRedirectView:
    def test_get_redirect_url(
        self, user: User, request_factory: RequestFactory
    ):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert (
            view.get_redirect_url() == f"/users/{user.username}/"
        )

def test_good_cheese_create_view(client, user):
    # Make the client authenticate
    client.force_login(user)
    # Specify the URL of the view
    url = reverse("cheeses:add")
    # Use the client to make the request
    response = client.get(url)
    # Test that the response is valid
    assert response.status_code == 200

# def test_cheese_list_contains_2_cheeses(rf):
#     # Let's create a couple cheeses
#     cheese1 = CheeseFactory()
#     cheese2 = CheeseFactory()
#     # Create a request and then a response
#     # for a list of cheeses
#     request = rf.get(reverse('cheeses:list'))
#     response = CheeseListView.as_view()(request)
#     # Assert that the response contains both cheese names
#     # in the template.
#     assertContains(response, cheese1.name)
#     assertContains(response, cheese2.name)
