import random
from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from Project_Management_System.analytics.models import Sprint
from Project_Management_System.Dashbords.models import Column, Dashbord
from Project_Management_System.Projects.models import Project
from Project_Management_System.Tasks.models import Task
from Project_Management_System.Users.models import User

# Fixtures ##############################################################


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


@pytest.fixture
def sprint(user, project):
    sprint = Sprint.objects.create(
        name="TestSprint",
        project=project,
        start_date=date(2025, 9, 7),
        end_date=date(2025, 9, 21),
    )
    return sprint


@pytest.fixture
def dashboard(project):
    dashboard = Dashbord.objects.create(name="TestDashboard", project=project)
    return dashboard


@pytest.fixture
def column(dashboard):
    column = Column.objects.create(name="TestColumn", order=1, dashbord=dashboard)
    return column


@pytest.fixture
def task(user, project, sprint, column):
    task = Task.objects.create(
        name="TestTaskName",
        description="",
        executor=user,
        author=user,
        project=project,
        sprint=sprint,
        story_points=random.randint(0, 20),
        column=column,
    )
    return task


# Tests #################################################################
@pytest.mark.django_db
def test_post_tasks(authenticated_client, user, project, sprint, column):
    url = reverse("tasks-list")
    data = {
        "name": "New Task",
        "description": "New Desc",
        "executor": user.id,
        "author": user.id,
        "project": project.id,
        "sprint": sprint.id,
        "story_points": 5,
        "column": column.id,
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    # assert response.data[0]["name"]=="New Task"


@pytest.mark.django_db
def test_get_all_tasks_authenicated(authenticated_client):
    url = reverse("tasks-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_all_tasks_unauthenicated(api_client):
    url = reverse("tasks-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_move_task(authenticated_client, task, dashboard):
    url = reverse("tasks-move", kwargs={"pk": task.pk})
    new_column = Column.objects.create(name="New Column", order=2, dashbord=dashboard)

    data = {"column": new_column.id}
    response = authenticated_client.post(url, data, format="json")
    task.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert task.column.id == new_column.id


@pytest.mark.django_db
def test_assign_task(authenticated_client, task):
    url = reverse("tasks-assign", kwargs={"pk": task.pk})
    new_user = User.objects.create(
        number="+111", username="NewUser", email="new@example.com"
    )
    data = {"executor": new_user.id}
    response = authenticated_client.post(url, data, format="json")
    task.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert task.executor.id == new_user.id


@pytest.mark.django_db
def test_subtask(authenticated_client, task):
    url = reverse("tasks-add-subtask", kwargs={"pk": task.pk})
    new_task = Task.objects.create(
        name=task.name,
        description="",
        executor=task.executor,
        author=task.author,
        project=task.project,
        sprint=task.sprint,
        story_points=random.randint(0, 20),
        column=task.column,
    )
    data = {"parent": new_task.id}
    response = authenticated_client.post(url, data, format="json")
    task.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"status": "subtask added"}


@pytest.mark.django_db
def test_update_task(authenticated_client, task):
    url = reverse("tasks-detail", kwargs={"pk": task.pk})
    data = {"name": "Updated Task Name"}
    response = authenticated_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.name == "Updated Task Name"


@pytest.mark.django_db
def test_delete_task(authenticated_client, task):
    url = reverse("tasks-detail", kwargs={"pk": task.pk})
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_create_invalid_task(authenticated_client, project):
    url = reverse("tasks-list")
    data = {"name": "", "description": "New Desc", "project": project.id}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
