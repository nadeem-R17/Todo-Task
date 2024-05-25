from django.test import TestCase
from task_list.serializers import ToDoSerializer
from task_list.models import ToDo
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class ToDoSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="username", password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.todo_attributes = {
            "title": "Test todo",
            "description": "Test description",
            "status": "OPEN",
            "tag": "tag1 tag2",
        }

        self.serializer_data = ToDoSerializer().data
        self.todo = ToDo.objects.create(**self.todo_attributes)
        self.serializer = ToDoSerializer(instance=self.todo)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "title",
                "description",
                "status",
                "tag",
                "timestamp",
                "due_date",
                "user",
            ],
        )

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], self.todo_attributes["title"])

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data["description"], self.todo_attributes["description"]
        )

    def test_status_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["status"], self.todo_attributes["status"])

    def test_tag_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            sorted(eval(data["tag"])),
            sorted(self.todo_attributes["tag"].split()),
        )
