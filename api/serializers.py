from datetime import timezone
from rest_framework import serializers
from .models import Poll, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    expired = serializers.SerializerMethodField()

    def get_expired(self, obj):
        return obj.expiry_date <= timezone.now()

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'choices', 'expired']
