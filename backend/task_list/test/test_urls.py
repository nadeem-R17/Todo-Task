from django.urls import reverse
from django.test import TestCase


class TodoURLsTestCase(TestCase):
    def test_create_todo_url(self):
        url = reverse("todo:create_todo")
        self.assertEqual(url, "/create/")

    def test_retrieve_todo_url(self):
        url = reverse("todo:retrieve_todo", args=[1])
        self.assertEqual(url, "/1/")

    def test_list_todos_url(self):
        url = reverse("todo:list_todos")
        self.assertEqual(url, "/")

    def test_update_todo_url(self):
        url = reverse("todo:update_todo", args=[1])
        self.assertEqual(url, "/1/update/")

    def test_delete_todo_url(self):
        url = reverse("todo:delete_todo", args=[1])
        self.assertEqual(url, "/1/delete/")
