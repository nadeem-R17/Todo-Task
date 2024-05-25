from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# custom field to store tags
class TagListField(models.TextField):
    def to_python(self, value):
        # if the value is already a list, return it as it is
        if isinstance(value, list):
            return value
        # if the value is a non-empty string, split it into a list of tags
        if value:
            return list(set(value.split(" ")))
        # if the value is None or an empty string, return an empty list
        return []

    # Prepare the value for saving to the database
    def get_prep_value(self, value):
        # If the value is a list or tuple, join it into a string of tags
        if isinstance(value, (list, tuple)):
            return " ".join(value)
        else:
            return value

    #  Convert the value from the database to a Python object
    def from_db_value(self, value, expression, connection):
        return self.to_python(value)


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    due_date = models.DateField(null=True, blank=True)
    tag = TagListField(blank=True, null=True)
    status = models.CharField(
        max_length=7,
        choices=[
            ("OPEN", "Open"),
            ("WORKING", "Working"),
            ("DONE", "Done"),
            ("OVERDUE", "Overdue"),
        ],
        default="OPEN",
    )

    def clean(self):
        super().clean()  # call the parent class's clean method

        # Check that due_date is not
        # before the creation time
        if (
            self.timestamp
            and self.due_date
            and self.due_date < self.timestamp.date()
        ):
            raise ValidationError(
                {"due_date": "Due date cannot be before the creation time."}
            )

    def save(self, *args, **kwargs):
        if not self.id:  # if the model instance has not been saved yet
            self.timestamp = (
                timezone.now()
            )  # set timestamp to the current time
        self.full_clean()  # validate the model instance
        super().save(*args, **kwargs)  # call the parent class's save method

    def __str__(self):
        return self.title
