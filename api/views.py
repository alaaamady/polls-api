from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer, VoteConfirmationSerializer
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.views import APIView


import environ


env = environ.Env()
environ.Env.read_env()


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'choices__text']
    ordering = ['-expiry_date']
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        return super().get_queryset().order_by('-expiry_date')


class VoteViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            choice_id = serializer.validated_data['choice_id']
            email = serializer.validated_data['email']
            try:
                choice = Choice.objects.get(id=choice_id)
            except Choice.DoesNotExist:
                return Response({'error': 'Choice does not exist.'}, status=status.HTTP_404_NOT_FOUND)

            vote = Vote.objects.create(
                choice=choice,
                email=email,
                otp=Vote.generate_otp()
            )
            send_mail(
                'Your One-Time Password for Voting',
                f'Your OTP is {vote.otp}. It will expire in 10 minutes.',
                env('EMAIL_ADDRESS'),
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteConfirmationView(APIView):
    def post(self, request):
        serializer = VoteConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uuid = serializer.validated_data['uuid']
        otp = serializer.validated_data['otp']

        try:
            vote = Vote.objects.get(uuid=uuid)
        except Vote.DoesNotExist:
            return Response({'error': 'Invalid vote UUID.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp != vote.otp:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        if vote.is_otp_expired():
            return Response({'error': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)

        vote.confirmed = True
        vote.save()
        return Response({'success': 'Vote confirmed.'})
