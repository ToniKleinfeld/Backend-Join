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

    def create(self, validated_data):
        subtasks_data = validated_data.pop("subtasks", [])
        assigned_users_data = validated_data.pop("assigned_users", [])

        task = Task.objects.create(**validated_data)

        if assigned_users_data:
            task.assigned_users.set(assigned_users_data)

        for subtask_data in subtasks_data:
            SubTask.objects.create(task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop("subtasks", None)
        assigned_users_data = validated_data.pop("assigned_users", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if assigned_users_data is not None:
            instance.assigned_users.set(assigned_users_data)

        if subtasks_data is not None:
            instance.subtasks.all().delete()

            for subtask_data in subtasks_data:
                SubTask.objects.create(task=instance, **subtask_data)

        return instance


class TaskWriteSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=False, write_only=True)
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
            assigned_users = User.objects.filter(id__in=assigned_user_ids)
            task.assigned_users.set(assigned_users)

        for subtask_item in subtasks_data:
            SubTask.objects.create(
                task=task,
                title=subtask_item.get("title", ""),
                done=subtask_item.get("done", False),
            )

        return task
