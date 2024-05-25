from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from .models import ToDo
from .serializers import ToDoSerializer
from rest_framework.response import Response


class CreateToDoView(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer


class RetrieveToDoView(RetrieveAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    lookup_field = "pk"


class UpdateToDoView(UpdateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        current_tag = instance.tag

        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        new_tag = serializer.validated_data.get("tag")

        if new_tag is not None:
            for i in range(len(current_tag)):
                if current_tag[i] not in new_tag:
                    new_tag += " " + (current_tag[i])

        serializer.validated_data["tag"] = new_tag
        self.perform_update(serializer)
        return Response(serializer.data)


class DeleteToDoView(DestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.all()
    lookup_field = "pk"


class ListToDoView(ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
