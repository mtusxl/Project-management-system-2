import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from Project_Management_System.Projects.models import Project
from Project_Management_System.Users.models import User

# Fixtures ##############################################################################


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user = User.objects.create(
        number="+0000000000", username="TestUser", email="testuseremail@gmail.com"
    )
    return user


@pytest.fixture
def access_token(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    return str(access_token)


@pytest.fixture
def authenticated_client(api_client, access_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def project(user):
    project = Project.objects.create(
        name="TestProject", description="TestDescription", author=user
    )
    project.members.add(user)
    return project


# Tests #################################################################################


@pytest.mark.django_db
def test_create_project(authenticated_client, user):
    url = reverse("projects-list")
    data = {
        "name": "TestProject",
        "Description": "Test Desc",
        "author": user.id,
        "members": [user.id],
    }
    response = authenticated_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.count() == 1


@pytest.mark.django_db
def test_get_projects(authenticated_client):
    url = reverse("projects-list")
    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_projects_unauthenicated(api_client):
    url = reverse("projects-list")
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_project(authenticated_client, project):
    url = reverse("projects-detail", kwargs={"pk": project.pk})
    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete(authenticated_client, project):
    url = reverse("projects-detail", kwargs={"pk": project.pk})
    response = authenticated_client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Project.objects.count() == 0


@pytest.mark.django_db
def test_update(authenticated_client, project):
    url = reverse("projects-detail", kwargs={"pk": project.pk})
    data = {"name": "Update name", "description": "Update Description"}

    response = authenticated_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Update name"
