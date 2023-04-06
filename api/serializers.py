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
    total_vote_count = serializers.SerializerMethodField()
    choices_with_vote_percentage = serializers.SerializerMethodField()

    def get_expired(self, obj):
        return obj.expiry_date <= timezone.now()

    def get_total_vote_count(self, obj):
        return Vote.objects.filter(choice__poll=obj).count()

    def get_choices_with_vote_percentage(self, obj):
        choices = obj.choices.all()
        vote_count = self.get_total_vote_count(obj)
        data = []
        for choice in choices:
            choice_vote_count = choice.votes.count()
            percentage = choice_vote_count / vote_count * 100 if vote_count > 0 else 0
            data.append({
                'choice_text': choice.text,
                'vote_count': choice_vote_count,
                'vote_percentage': percentage
            })
        return data

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'expired', 'expiry_date',
                  'total_vote_count', 'choices_with_vote_percentage']


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
