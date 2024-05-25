from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from task_list.models import ToDo


class ToDoIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="nadeemraza", password="password"
        )
        self.client.force_authenticate(user=self.user)

        self.create_url = reverse("todo:create_todo")
        self.list_url = reverse("todo:list_todos")

    def test_create_and_retrieve_todo(self):
        # Test creating a new todo
        data = {
            "title": "Test todo",
            "description": "Test description",
            "status": "OPEN",
            "tag": "tag1 tag2",
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDo.objects.count(), 1)
        todo = ToDo.objects.get()
        self.assertEqual(todo.title, "Test todo")

        # Test retrieving the created todo
        retrieve_url = reverse("todo:retrieve_todo", args=[todo.pk])
        response = self.client.get(retrieve_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test todo")

    def test_update_todo(self):
        # Create a new todo
        todo = ToDo.objects.create(
            title="Test todo",
            description="Test description",
            status="OPEN",
            tag="tag1 tag2",
        )

        # Test updating the created todo
        update_url = reverse("todo:update_todo", args=[todo.pk])
        data = {
            "title": "Updated todo",
            "description": "This is an updated todo description",
            "status": "WORKING",
            "tag": "tag1 tag2 tag3",
        }
        response = self.client.patch(update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_todo = ToDo.objects.get(pk=todo.pk)
        self.assertEqual(updated_todo.title, "Updated todo")

    def test_delete_todo(self):
        # Create a new todo
        todo = ToDo.objects.create(
            title="Test todo",
            description="Test description",
            status="OPEN",
            tag="tag1 tag2",
        )

        # Test deleting the created todo
        delete_url = reverse("todo:delete_todo", args=[todo.pk])
        response = self.client.delete(delete_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ToDo.objects.count(), 0)

    def test_list_todos(self):
        # Create some todos
        ToDo.objects.create(
            title="Test todo 1",
            description="Test description 1",
            status="OPEN",
            tag="tag1 tag2",
        )
        ToDo.objects.create(
            title="Test todo 2",
            description="Test description 2",
            status="OPEN",
            tag="tag3 tag4",
        )

        # Test listing all todos
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
