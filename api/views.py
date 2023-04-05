from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer
from django.core.mail import send_mail
from django.utils import timezone


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
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
