from django.test import TestCase
from task_list.models import ToDo
from django.db import models
from task_list.models import TagListField
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class ToDoModelTest(TestCase):
    def setUp(self):
        self.field = TagListField()

    def test_to_python_with_list(self):
        value = ["tag1", "tag2", "tag3"]
        result = self.field.to_python(value)
        self.assertEqual(result, value)

    def test_to_python_with_string(self):
        value = "tag1 tag2 tag3 tag1"
        expected_result = ["tag1", "tag2", "tag3"]
        result = self.field.to_python(value)
        self.assertEqual(set(result), set(expected_result))

    def test_to_python_with_empty_string(self):
        value = ""
        expected_result = []
        result = self.field.to_python(value)
        self.assertEqual(result, expected_result)

    def test_to_python_with_none(self):
        value = None
        expected_result = []
        result = self.field.to_python(value)
        self.assertEqual(result, expected_result)

    def test_get_prep_value_with_list(self):
        value = ["tag1", "tag2", "tag3"]
        expected_result = "tag1 tag2 tag3"
        result = self.field.get_prep_value(value)
        self.assertEqual(result, expected_result)

    def test_get_prep_value_with_empty_list(self):
        value = []
        expected_result = ""
        result = self.field.get_prep_value(value)
        self.assertEqual(result, expected_result)

    def test_get_prep_value_with_none(self):
        value = None
        expected_result = None
        result = self.field.get_prep_value(value)
        self.assertEqual(result, expected_result)

    def test_string_representation(self):
        todo = ToDo(title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")

    def test_field_length(self):
        max_length = ToDo._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_description_string_representation(self):
        todo = ToDo(description="This is a Test Todo")
        self.assertEqual(todo.description, "This is a Test Todo")

    def test_description_field_length(self):
        max_length = ToDo._meta.get_field("description").max_length
        self.assertEqual(max_length, 1000)

    def test_tag_list_field(self):
        tag_list_field = ToDo._meta.get_field("tag")
        self.assertIsInstance(tag_list_field, models.TextField)

    def test_status_choices(self):
        status_choices = [
            ("OPEN", "Open"),
            ("WORKING", "Working"),
            ("DONE", "Done"),
            ("OVERDUE", "Overdue"),
        ]
        self.assertEqual(
            ToDo._meta.get_field("status").choices, status_choices
        )

    def test_due_date_blank_and_null(self):
        due_date_field = ToDo._meta.get_field("due_date")
        self.assertTrue(due_date_field.blank)
        self.assertTrue(due_date_field.null)

    def test_timestamp_auto_now_add(self):
        timestamp_field = ToDo._meta.get_field("timestamp")
        self.assertTrue(timestamp_field.auto_now_add)

    def test_due_date_before_creation_date(self):
        # Create a ToDo instance with due_date before creation_date
        todo = ToDo(
            title="Test todo",
            description="Test description",
            status="OPEN",
            tag="tag1 tag2",
            due_date=datetime.now() - timedelta(days=10),  # 10 days before now
        )
        # Assert that saving the todo raises a ValidationError
        with self.assertRaises(ValidationError):
            todo.save()
