from django.utils import timezone
from rest_framework import serializers
from .models import Poll, Choice, Vote


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
        fields = ['id', 'title', 'description',
                  'choices', 'expired', 'expiry_date']


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()
    email = serializers.EmailField()
    poll_id = serializers.IntegerField()

    def validate_choice_id(self, value):
        try:
            Choice.objects.get(id=value)
        except Choice.DoesNotExist:
            raise serializers.ValidationError('Choice does not exist.')
        return value

    def validate_email(self, value):
        try:
            poll_id = self.initial_data['poll_id']
            Vote.objects.get(
                email=value, choice__poll=poll_id)
        except Vote.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                'You have already voted on this poll.')
        return value


class VoteConfirmationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    uuid = serializers.UUIDField()

    def validate_uuid(self, value):
        try:
            Vote.objects.get(uuid=value)
        except Vote.DoesNotExist:
            raise serializers.ValidationError('Invalid vote UUID.')
        return value
