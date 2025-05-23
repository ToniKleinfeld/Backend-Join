from django.contrib.auth.models import User
from rest_framework import serializers
from join_app.models import Contact, Task, SubTask
from join_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["color"]


class UserSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source="profile.color", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "color"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "email", "phone", "bgcolor"]


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ["id", "task", "title", "done"]
        read_only_fields = ["task"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Tasks Serializer für Tasks Abfragen , Löschen
    """
    creator = UserSerializer(read_only=True)
    subtasks = SubTaskSerializer(many=True, required=False)
    assigned_users = UserSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "creator",
            "title",
            "description",
            "rubric",
            "category",
            "prio",
            "due_date",
            "assigned_users",
            "subtasks",
        ]


class TaskWriteSerializer(serializers.ModelSerializer):
    """
    Tasks Serializer zum Erstellen , Abändern
    """
    subtasks = SubTaskSerializer(many=True, required=False)
    assigned_users = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "rubric",
            "category",
            "prio",
            "due_date",
            "assigned_users",
            "subtasks",
        ]

    def validate_rubric(self, value):
        valid_values = dict(Task.RUBRIC_CHOICES).keys()
        if value not in valid_values:
            raise serializers.ValidationError(
                f"Ungültiger Rubrik-Wert. Muss einer dieser Werte sein: {valid_values}"
            )
        return value

    def validate_category(self, value):
        valid_values = dict(Task.CATEGORY_CHOICES).keys()
        if value not in valid_values:
            raise serializers.ValidationError(
                f"Ungültiger Kategorie-Wert. Muss einer dieser Werte sein: {valid_values}"
            )
        return value

    def validate_prio(self, value):
        valid_values = dict(Task.PRIORITY_CHOICES).keys()
        if value not in valid_values:
            raise serializers.ValidationError(
                f"Ungültiger Prioritätswert. Muss einer dieser Werte sein: {valid_values}"
            )
        return value

    def create(self, validated_data):
        subtasks_data = validated_data.pop("subtasks", [])
        assigned_user_ids = validated_data.pop("assigned_users", [])

        task = Task.objects.create(**validated_data)

        if assigned_user_ids:
            user = User.objects.filter(id__in=assigned_user_ids)
            task.assigned_users.set(user)

        for subtask_item in subtasks_data:
            SubTask.objects.create(
                task=task,
                title=subtask_item.get("title", ""),
                done=subtask_item.get("done", False),
            )

        return task
    
    def update(self, instance, validated_data):
        assigned_user_ids = validated_data.pop("assigned_users", None)
        subtasks_data = validated_data.pop("subtasks", None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if assigned_user_ids is not None:
            users = User.objects.filter(pk__in=assigned_user_ids)
            instance.assigned_users.set(users)

        if subtasks_data is not None:
            instance.subtasks.all().delete()
            for sub in subtasks_data:
                SubTask.objects.create(task=instance, **sub)

        return instance