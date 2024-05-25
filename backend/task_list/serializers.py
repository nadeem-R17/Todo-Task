from rest_framework import serializers
from .models import ToDo, TagListField


class ToDoSerializer(serializers.ModelSerializer):
    tags = TagListField()

    class Meta:
        model = ToDo
        fields = "__all__"
