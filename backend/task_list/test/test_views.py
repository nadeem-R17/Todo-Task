from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from task_list.models import ToDo
from django.contrib.auth.models import User


class TestCreateToDoView(TestCase):
    def setUp(self):
        # Creating an APIClient instance to use in the tests
        self.client = APIClient()
        # Creating a User instance to use in the tests
        self.user = User.objects.create_user(
            username="username", password="password"
        )
        # Authenticate the client with the user
        self.client.force_authenticate(user=self.user)

    def test_create_todo(self):
        url = reverse("todo:create_todo")
        data = {
            "title": "Test todo",
            "description": "Test description",
            "status": "OPEN",
            "tag": "tag1 tag2",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDo.objects.count(), 1)
        self.assertEqual(ToDo.objects.get().title, "Test todo")


class TestRetrieveToDoView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="username", password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.todo = ToDo.objects.create(
            title="Test todo",
            description="Test description",
            status="OPEN",
            tag="tag1 tag2",
        )

    def test_retrieve_todo(self):
        url = reverse("todo:retrieve_todo", args=[self.todo.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test todo")


class TestListToDoView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="username", password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.todo1 = ToDo.objects.create(
            title="Test todo 1",
            description="Test description 1",
            status="OPEN",
            tag="tag1 tag2",
        )
        self.todo2 = ToDo.objects.create(
            title="Test todo 2",
            description="Test description 2",
            status="OPEN",
            tag="tag3 tag4",
        )

    def test_list_todo(self):
        url = reverse("todo:list_todos")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TestUpdateToDoView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="username", password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.todo = ToDo.objects.create(
            title="Test todo",
            description="Test description",
            status="OPEN",
            tag="tag1 tag2",
        )
        self.url = reverse("todo:update_todo", args=[self.todo.pk])

    def test_update_todo(self):
        data = {
            "title": "Updated todo",
            "description": "This is an updated todo description",
            "status": "WORKING",
            "tag": "tag1 tag2 tag3",
        }
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ToDo.objects.count(), 1)
        updated_todo = ToDo.objects.get(pk=self.todo.pk)
        self.assertEqual(updated_todo.title, "Updated todo")
        self.assertEqual(
            updated_todo.description, "This is an updated todo description"
        )
        self.assertEqual(updated_todo.status, "WORKING")
        self.assertEqual(" ".join(sorted(updated_todo.tag)), "tag1 tag2 tag3")

    def test_update_todo_with_existing_tags(self):
        data = {
            "title": "Updated todo",
            "description": "This is an updated todo description",
            "status": "WORKING",
            "tag": "tag3",
        }
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ToDo.objects.count(), 1)
        updated_todo = ToDo.objects.get(pk=self.todo.pk)
        self.assertEqual(updated_todo.title, "Updated todo")
        self.assertEqual(
            updated_todo.description, "This is an updated todo description"
        )
        self.assertEqual(updated_todo.status, "WORKING")
        self.assertEqual(" ".join(sorted(updated_todo.tag)), "tag1 tag2 tag3")


class TestDeleteToDoView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="username", password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.todo = ToDo.objects.create(
            title="Test todo",
            description="Test description",
            status="OPEN",
            tag="tag1 tag2",
        )

    def test_delete_todo(self):
        url = reverse("todo:delete_todo", args=[self.todo.pk])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ToDo.objects.count(), 0)
